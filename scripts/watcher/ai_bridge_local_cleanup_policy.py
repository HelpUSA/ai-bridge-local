#!/usr/bin/env python3
import argparse
from pathlib import Path

CONFIRM_TOKEN = 'AI_BRIDGE_LOCAL_DELETE_TEMP_SCRIPTS'

def collect_files(path: Path):
    if not path.exists():
        return []
    return sorted(
        [p for p in path.iterdir() if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='temp/watcher_scripts')
    parser.add_argument('--keep', type=int, default=30)
    parser.add_argument('--delete', action='store_true')
    parser.add_argument('--confirm', default='')
    args = parser.parse_args()

    print('AI_BRIDGE_LOCAL_CLEANUP_POLICY_START')
    path = Path(args.dir)
    print('DIR|' + str(path))
    print('KEEP|' + str(args.keep))
    print('DELETE|' + str(args.delete))

    if args.keep < 1:
        print('ERROR|keep_must_be_at_least_1')
        raise SystemExit(2)

    files = collect_files(path)
    print('TOTAL_BEFORE|' + str(len(files)))

    stale = files[args.keep:]
    if args.delete and args.confirm != CONFIRM_TOKEN:
        print('ERROR|missing_confirm_token')
        print('EXPECTED_CONFIRM|' + CONFIRM_TOKEN)
        raise SystemExit(2)

    for item in stale:
        action = 'DELETE' if args.delete else 'WOULD_DELETE'
        print(action + '|' + item.name + '|' + str(item.stat().st_size))
        if args.delete:
            item.unlink()

    after = collect_files(path)
    print('TOTAL_AFTER|' + str(len(after)))
    print('AI_BRIDGE_LOCAL_CLEANUP_POLICY_END')

if __name__ == '__main__':
    main()
