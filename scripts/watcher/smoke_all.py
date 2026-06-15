from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
WATCHER = ROOT / "scripts" / "watcher"

SKIP = {
    "smoke_all.py",
    "smoke_command_accepted_progress_notice.py",
    "smoke_composer_submit_guard.py",
    "smoke_disable_worker_running_notice.py",
    "smoke_gateway_feedback_dedup.py",
    "smoke_rollback_helper.py",
}

def main() -> int:
    smoke_files = []
    skipped = []

    for path in sorted(WATCHER.glob("smoke_*.py")):
        if path.name in SKIP:
            skipped.append(path)
            continue
        smoke_files.append(path)

    if not smoke_files:
        print("NO_SMOKES_FOUND")
        return 1

    failed = []
    for path in smoke_files:
        rel = path.relative_to(ROOT).as_posix()
        print("")
        print("--- RUN " + rel + " ---")
        result = subprocess.run([sys.executable, str(path)], cwd=str(ROOT))
        if result.returncode != 0:
            failed.append((rel, result.returncode))

    if skipped:
        print("")
        print("SKIPPED_LEGACY_SMOKES")
        for path in skipped:
            print(path.relative_to(ROOT).as_posix())

    if failed:
        print("")
        print("FAILED_SMOKES")
        for rel, code in failed:
            print(rel + " code=" + str(code))
        return 1

    print("")
    print("OK smoke_all " + str(len(smoke_files)) + " files skipped=" + str(len(skipped)))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())