#!/usr/bin/env python3
import argparse
import subprocess
import sys

def run(cmd, title):
    print('SECTION|' + title)
    print('RUN|' + ' '.join(cmd))
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-smoke', action='store_true')
    parser.add_argument('--cleanup-keep', type=int, default=30)
    args = parser.parse_args()

    print('AI_BRIDGE_LOCAL_OPS_REPORT_START')
    run(['git', 'status', '-sb'], 'git_status')
    run(['git', 'log', '--oneline', '-12'], 'git_log')
    run(['git', 'tag', '--list', 'v0.4.*', '--sort=-creatordate'], 'git_tags')
    run([sys.executable, 'scripts/watcher/ai_bridge_local_filtered_db_status.py', '--limit', '25'], 'filtered_db_status')
    run([sys.executable, 'scripts/watcher/ai_bridge_local_db_status.py'], 'full_db_status')
    run([sys.executable, 'scripts/watcher/ai_bridge_local_cleanup_watcher_scripts.py', '--keep', str(args.cleanup_keep)], 'cleanup_dry_run')
    if not args.skip_smoke:
        run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/watcher/ai_bridge_local_smoke_0417.ps1'], 'smoke_0417')
    run(['git', 'diff', '--check'], 'diff_check')
    print('AI_BRIDGE_LOCAL_OPS_REPORT_END')

if __name__ == '__main__':
    main()
