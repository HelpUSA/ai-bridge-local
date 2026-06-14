import argparse
import json
LESSONS = {'teach_watcher_basics': {'title': 'Watcher basics', 'steps': ['Use strict JSON envelope markers', 'Prefer read-only inspection first', 'Use script_ext and script_text for multi-line commands', 'Check status after every run']}, 'teach_repo_safety': {'title': 'Repository safety', 'steps': ['Start with git status -sb', 'Read diffs before patching', 'Avoid broad cleanup commands', 'Validate before commit and push']}, 'teach_release_flow': {'title': 'Release flow', 'steps': ['Bump VERSION and extension versions', 'Run smokes and release_check', 'Commit release changes', 'Tag release commit', 'Push branch and tag', 'Update guide commit reference']}, 'teach_failure_recovery': {'title': 'Failure recovery', 'steps': ['Read exact stderr', 'Do not reset blindly', 'Patch the smallest failing point', 'Run the failed smoke again', 'Audit clean state after recovery']}}
parser = argparse.ArgumentParser(description='Render AI Bridge Local teaching envelopes.')
parser.add_argument('lesson', nargs='?', default='all')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
if args.lesson != 'all' and args.lesson not in LESSONS: raise SystemExit('unknown lesson: ' + args.lesson)
selected = LESSONS if args.lesson == 'all' else {args.lesson: LESSONS[args.lesson]}
payload = {'schema': 'ai_bridge_local.teach_envelopes', 'schema_version': 1, 'lessons': selected}
if args.json: print(json.dumps(payload, ensure_ascii=False, indent=2)); raise SystemExit(0)
lines = []
[lines.extend(['AI_BRIDGE_LOCAL_TEACH ' + key, lesson['title']] + ['- ' + step for step in lesson['steps']] + ['']) for key, lesson in selected.items()]
print(chr(10).join(lines))
