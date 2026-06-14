
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
print("PATCH_INTENT_PAYLOAD_SUPPORT_START")

def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")

def patch_gateway() -> None:
    path = ROOT / "gateway_local.py"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    changed = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            stripped.startswith("if not payload.get")
            and "payload.get('command')" in stripped
            and "payload.get('script_text')" in stripped
            and "payload.get('script_path')" in stripped
            and "payload.get('intent')" not in stripped
        ):
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = (
                indent
                + "if not payload.get('command') and not payload.get('script_text') "
                + "and not payload.get('script_path') and not payload.get('intent'):"
            )
            changed = True
            break
    if not changed:
        raise SystemExit("gateway validation target not found or already patched")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def patch_worker() -> None:
    path = ROOT / "brain_worker.py"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith("def execute_command("):
            start = i
            continue
        if start is not None and i > start and line.startswith("def "):
            end = i
            break
    if start is None:
        raise SystemExit("execute_command start not found")
    if end is None:
        end = len(lines)
    new_block = """
def execute_command(payload, command_id="unknown"):
    if not isinstance(payload, dict):
        return {"return_code": -1, "stdout": "", "stderr": "invalid_payload_not_object"}

    intent = payload.get("intent")
    if intent and not payload.get("command") and not payload.get("script_text") and not payload.get("script_path"):
        intent_command = [
            "python",
            "scripts/watcher/command_intake.py",
            "--intent",
            str(intent),
            "--command-id",
            str(command_id),
            "--cwd",
            str(payload.get("cwd") or "."),
        ]
        if payload.get("execute_intent"):
            intent_command.append("--execute")
        if payload.get("timeout_seconds"):
            intent_command.extend(["--timeout", str(int(payload.get("timeout_seconds")))])
        payload = dict(payload)
        payload["command"] = intent_command

    script_path = prepare_temp_script(payload, command_id)
    cmd = normalize_command(payload.get("command"))
    if script_path:
        if not cmd:
            if script_path.lower().endswith(".ps1"):
                cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path]
            elif script_path.lower().endswith(".py"):
                cmd = ["python", script_path]
            else:
                cmd = [script_path]
        else:
            cmd = [str(x).replace("{script_path}", script_path) for x in cmd]
    cwd = payload.get("cwd") or "."
    timeout = int(payload.get("timeout_seconds") or 30)
    if not cmd:
        return {"return_code": -1, "stdout": "", "stderr": "missing_payload_command"}
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {"return_code": result.returncode, "stdout": truncate(result.stdout), "stderr": truncate(result.stderr)}
    except subprocess.TimeoutExpired:
        return {"return_code": -1, "stdout": "", "stderr": "timeout"}
    except Exception as exc:
        return {"return_code": -1, "stdout": "", "stderr": str(exc)}
""".strip("\n").splitlines()
    patched = lines[:start] + new_block + lines[end:]
    path.write_text("\n".join(patched) + "\n", encoding="utf-8")

def write_smoke() -> None:
    smoke = """
from brain_worker import execute_command

result = execute_command({"cwd": ".", "timeout_seconds": 120, "intent": "inspect_repo"}, "smoke_intent_payload")
assert result["return_code"] == 0, result
assert "inspect_repo" in result["stdout"], result["stdout"]
assert "ai_bridge_local.command_intake_plan" in result["stdout"], result["stdout"]

executed = execute_command({"cwd": ".", "timeout_seconds": 120, "intent": "run_smokes", "execute_intent": True}, "smoke_intent_payload_execute")
assert executed["return_code"] == 0, executed
assert '"status": "acked"' in executed["stdout"], executed["stdout"]

print("OK intent_payload_smoke")
""".lstrip()
    write("scripts/watcher/smoke_intent_payload.py", smoke)

def update_release_scripts() -> None:
    marker = "smoke_intent_payload.py"
    addition = "\npython scripts/watcher/smoke_intent_payload.py\nif($LASTEXITCODE -ne 0){exit $LASTEXITCODE}\n"
    for name in ["scripts/watcher/release_check.ps1", "scripts/watcher/validate_all.ps1"]:
        path = ROOT / name
        text = path.read_text(encoding="utf-8", errors="replace")
        if marker not in text:
            text = text.rstrip() + "\n" + addition
            path.write_text(text, encoding="utf-8")

def run(cmd):
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, check=True)

patch_gateway()
patch_worker()
write_smoke()
update_release_scripts()

run([sys.executable, "-m", "py_compile", "gateway_local.py", "brain_worker.py", "scripts/watcher/smoke_intent_payload.py"])
run([sys.executable, "scripts/watcher/smoke_intent_payload.py"])
run([sys.executable, "scripts/watcher/bump_version.py", "0.4.44"])
run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "scripts/watcher/release_check.ps1"])
run(["git", "diff", "--check"])
run(["git", "diff", "--stat"])
run(["git", "add", "VERSION", "extension/manifest.json", "gateway_local.py", "brain_worker.py", "scripts/watcher/smoke_intent_payload.py", "scripts/watcher/release_check.ps1", "scripts/watcher/validate_all.ps1", "scripts/watcher/patch_intent_payload_support.py"])
run(["git", "commit", "-m", "Add intent payload support"])
run(["git", "tag", "-a", "v0.4.44-intent-payload", "-m", "v0.4.44 intent payload"])
run(["git", "push"])
run(["git", "push", "origin", "v0.4.44-intent-payload"])
run(["git", "status", "-sb"])
print("PATCH_INTENT_PAYLOAD_SUPPORT_END")
