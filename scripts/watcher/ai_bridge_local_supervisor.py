#!/usr/bin/env python3
"""AI Bridge Local process supervisor.

Keeps gateway_local.py and brain_worker.py observable and can restart missing
processes. Version 0.4.28 adds safe worker dedupe: only Python processes whose
command line contains brain_worker.py are candidates, so the active PowerShell
command process is never selected as a worker.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple, Dict, Any

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "logs" / "supervisor"
GATEWAY_SCRIPT = "gateway_local.py"
WORKER_SCRIPT = "brain_worker.py"
PORT = "8766"


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def run(cmd: List[str]) -> Tuple[int, str, str]:
    cp = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return cp.returncode, cp.stdout.strip(), cp.stderr.strip()


def ps_json(filter_expr: str) -> List[Dict[str, Any]]:
    ps = (
        "Get-CimInstance Win32_Process -Filter "
        + repr(filter_expr)
        + " | Select-Object ProcessId,ParentProcessId,CreationDate,Name,CommandLine"
        + " | ConvertTo-Json -Compress"
    )
    code, out, err = run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps])
    if code != 0 or not out:
        return []
    data = json.loads(out)
    if isinstance(data, dict):
        data = [data]
    return data


def gateway_processes() -> List[Dict[str, Any]]:
    return ps_json("Name LIKE 'python%' AND CommandLine LIKE '%gateway_local.py%'")


def worker_processes() -> List[Dict[str, Any]]:
    return ps_json("Name LIKE 'python%' AND CommandLine LIKE '%brain_worker.py%'")


def port_owner() -> str:
    code, out, err = run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", f"netstat -ano | findstr ':{PORT}'"])
    return out or err or ""


def log(msg: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"{now()} {msg}"
    print(line)
    with (LOG_DIR / "ai_bridge_local_supervisor.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def start_process(script: str) -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stdout_path = LOG_DIR / f"{Path(script).stem}.stdout.log"
    stderr_path = LOG_DIR / f"{Path(script).stem}.stderr.log"
    out = stdout_path.open("a", encoding="utf-8")
    err = stderr_path.open("a", encoding="utf-8")
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    proc = subprocess.Popen(
        [sys.executable, script],
        cwd=str(ROOT),
        stdout=out,
        stderr=err,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    log(f"STARTED script={script} pid={proc.pid}")
    return proc.pid


def short_cmd(proc: Dict[str, Any]) -> str:
    return str(proc.get("CommandLine") or "")[:300]


def report() -> int:
    gateway = gateway_processes()
    worker = worker_processes()
    print("AI_BRIDGE_LOCAL_SUPERVISOR_REPORT_START")
    print("ROOT|" + str(ROOT))
    print("GATEWAY_COUNT|" + str(len(gateway)))
    for item in gateway:
        print("GATEWAY|" + str(item.get("ProcessId")) + "|" + short_cmd(item))
    print("WORKER_COUNT|" + str(len(worker)))
    for item in worker:
        print("WORKER|" + str(item.get("ProcessId")) + "|ppid=" + str(item.get("ParentProcessId")) + "|" + short_cmd(item))
    print("PORT_8766")
    port = port_owner()
    print(port if port else "NO_PORT_ENTRY")
    print("AI_BRIDGE_LOCAL_SUPERVISOR_REPORT_END")
    if len(gateway) == 1 and len(worker) == 1:
        return 0
    return 2


def choose_worker_to_keep(workers: List[Dict[str, Any]]) -> int:
    parent_pid = os.getppid()
    worker_ids = {int(w.get("ProcessId")) for w in workers}
    if parent_pid in worker_ids:
        return parent_pid
    def key(item: Dict[str, Any]) -> str:
        return str(item.get("CreationDate") or "")
    oldest = sorted(workers, key=key)[0]
    return int(oldest.get("ProcessId"))


def dedupe_workers() -> int:
    workers = worker_processes()
    print("AI_BRIDGE_LOCAL_WORKER_DEDUPE_START")
    print("WORKER_COUNT_BEFORE|" + str(len(workers)))
    for item in workers:
        print("WORKER_BEFORE|" + str(item.get("ProcessId")) + "|ppid=" + str(item.get("ParentProcessId")) + "|" + short_cmd(item))
    if len(workers) <= 1:
        print("NO_DEDUPE_NEEDED")
        print("AI_BRIDGE_LOCAL_WORKER_DEDUPE_END")
        return 0
    keep = choose_worker_to_keep(workers)
    print("KEEP_WORKER_PID|" + str(keep))
    for item in workers:
        pid = int(item.get("ProcessId"))
        if pid == keep:
            continue
        print("STOPPING_DUPLICATE_WORKER|" + str(pid))
        code, out, err = run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", f"Stop-Process -Id {pid} -Force"])
        print("STOP_RETURN|" + str(pid) + "|" + str(code))
        if err:
            print("STOP_STDERR|" + err)
    time.sleep(2)
    after = worker_processes()
    print("WORKER_COUNT_AFTER|" + str(len(after)))
    for item in after:
        print("WORKER_AFTER|" + str(item.get("ProcessId")) + "|ppid=" + str(item.get("ParentProcessId")) + "|" + short_cmd(item))
    print("AI_BRIDGE_LOCAL_WORKER_DEDUPE_END")
    return 0 if len(after) == 1 else 2


def supervise_once(no_start: bool = False, dedupe: bool = False) -> int:
    gateway = gateway_processes()
    worker = worker_processes()
    log(f"CHECK gateway_count={len(gateway)} worker_count={len(worker)} no_start={no_start} dedupe={dedupe}")
    if not no_start:
        if len(gateway) == 0:
            start_process(GATEWAY_SCRIPT)
        if len(worker) == 0:
            start_process(WORKER_SCRIPT)
    if dedupe:
        dedupe_workers()
    return report()


def main() -> int:
    ap = argparse.ArgumentParser(description="AI Bridge Local gateway/worker supervisor")
    ap.add_argument("--once", action="store_true", help="run one check and exit")
    ap.add_argument("--loop", action="store_true", help="keep checking and restart missing processes")
    ap.add_argument("--interval", type=int, default=15, help="seconds between loop checks")
    ap.add_argument("--no-start", action="store_true", help="only report; do not start missing processes")
    ap.add_argument("--status", action="store_true", help="print process report and exit")
    ap.add_argument("--dedupe", action="store_true", help="stop duplicate Python brain_worker.py processes, keeping current parent worker or oldest")
    args = ap.parse_args()

    if args.status:
        return report()
    if args.dedupe and not args.loop and not args.once:
        return dedupe_workers()
    if args.loop:
        log("LOOP_START interval=" + str(args.interval))
        while True:
            supervise_once(no_start=args.no_start, dedupe=args.dedupe)
            time.sleep(max(3, args.interval))
    return supervise_once(no_start=args.no_start, dedupe=args.dedupe)


if __name__ == "__main__":
    raise SystemExit(main())
