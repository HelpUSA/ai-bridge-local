#!/usr/bin/env python3
"""AI Bridge Local process supervisor.

Keeps gateway_local.py and brain_worker.py observable and optionally restarts
missing processes. Designed for Windows/local use in D:/dev/autocode/ai-bridge-local.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "logs" / "supervisor"
GATEWAY_SCRIPT = "gateway_local.py"
WORKER_SCRIPT = "brain_worker.py"
PORT = "8766"


def now() -> str:
    return _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def run(cmd: List[str]) -> Tuple[int, str, str]:
    cp = subprocess.run(cmd, cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return cp.returncode, cp.stdout.strip(), cp.stderr.strip()


def ps_processes() -> List[Tuple[int, str]]:
    ps = "Get-CimInstance Win32_Process | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
    code, out, err = run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps])
    if code != 0 or not out:
        return []
    import json
    data = json.loads(out)
    if isinstance(data, dict):
        data = [data]
    items: List[Tuple[int, str]] = []
    for item in data:
        cmd = item.get("CommandLine") or ""
        pid = item.get("ProcessId")
        if pid is None:
            continue
        items.append((int(pid), cmd))
    return items


def matching(name: str) -> List[Tuple[int, str]]:
    needle = name.lower()
    out = []
    for pid, cmd in ps_processes():
        low = cmd.lower()
        if needle in low and "ai_bridge_local_supervisor.py" not in low:
            out.append((pid, cmd))
    return out


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
    proc = subprocess.Popen([sys.executable, script], cwd=str(ROOT), stdout=out, stderr=err, stdin=subprocess.DEVNULL, creationflags=creationflags)
    log(f"STARTED script={script} pid={proc.pid}")
    return proc.pid


def report() -> int:
    gateway = matching(GATEWAY_SCRIPT)
    worker = matching(WORKER_SCRIPT)
    print("AI_BRIDGE_LOCAL_SUPERVISOR_REPORT_START")
    print("ROOT|" + str(ROOT))
    print("GATEWAY_COUNT|" + str(len(gateway)))
    for pid, cmd in gateway:
        print("GATEWAY|" + str(pid) + "|" + cmd[:300])
    print("WORKER_COUNT|" + str(len(worker)))
    for pid, cmd in worker:
        print("WORKER|" + str(pid) + "|" + cmd[:300])
    print("PORT_8766")
    port = port_owner()
    print(port if port else "NO_PORT_ENTRY")
    print("AI_BRIDGE_LOCAL_SUPERVISOR_REPORT_END")
    if len(gateway) == 1 and len(worker) == 1:
        return 0
    return 2


def supervise_once(no_start: bool = False) -> int:
    gateway = matching(GATEWAY_SCRIPT)
    worker = matching(WORKER_SCRIPT)
    log(f"CHECK gateway_count={len(gateway)} worker_count={len(worker)} no_start={no_start}")
    if not no_start:
        if len(gateway) == 0:
            start_process(GATEWAY_SCRIPT)
        if len(worker) == 0:
            start_process(WORKER_SCRIPT)
    return report()


def main() -> int:
    ap = argparse.ArgumentParser(description="AI Bridge Local gateway/worker supervisor")
    ap.add_argument("--once", action="store_true", help="run one check and exit")
    ap.add_argument("--loop", action="store_true", help="keep checking and restart missing processes")
    ap.add_argument("--interval", type=int, default=15, help="seconds between loop checks")
    ap.add_argument("--no-start", action="store_true", help="only report; do not start missing processes")
    ap.add_argument("--status", action="store_true", help="print process report and exit")
    args = ap.parse_args()

    if args.status:
        return report()
    if args.loop:
        log("LOOP_START interval=" + str(args.interval))
        while True:
            supervise_once(no_start=args.no_start)
            time.sleep(max(3, args.interval))
    return supervise_once(no_start=args.no_start)


if __name__ == "__main__":
    raise SystemExit(main())
