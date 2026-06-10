#!/usr/bin/env python3
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep", type=int, default=30)
    parser.add_argument("--dir", default="temp/watcher_scripts")
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args()

    print("AI_BRIDGE_LOCAL_CLEANUP_WATCHER_SCRIPTS_START")
    path = Path(args.dir)
    if not path.exists():
        print("NO_TEMP_WATCHER_SCRIPTS_DIR")
        return

    files = sorted(
        [p for p in path.iterdir() if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    print(f"TOTAL_BEFORE={len(files)}")
    print(f"KEEP={args.keep}")
    print(f"MODE={'DELETE' if args.delete else 'DRY_RUN'}")

    stale = files[args.keep:]
    for item in stale:
        print(f"{'DELETE' if args.delete else 'WOULD_DELETE'}|{item.name}|{item.stat().st_size}")
        if args.delete:
            item.unlink()

    after = len([p for p in path.iterdir() if p.is_file()])
    print(f"TOTAL_AFTER={after}")
    print("AI_BRIDGE_LOCAL_CLEANUP_WATCHER_SCRIPTS_END")

if __name__ == "__main__":
    main()
