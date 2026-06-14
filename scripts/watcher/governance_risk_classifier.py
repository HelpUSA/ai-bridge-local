import argparse
import json
parser = argparse.ArgumentParser(description='Read-only watcher command risk classifier.')
parser.add_argument('--command', default='')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
cmd = args.command.lower()
destructive_terms = ['remove-item', 'rm -rf', 'del /q', 'rmdir', 'format', 'drop table', 'reset --hard', 'clean -fd', 'erase']
mutation_terms = ['git commit', 'git push', 'set-content', 'add-content', 'writealltext', 'new-item', 'move-item', 'copy-item', '--apply']
dry_terms = ['dry-run', '--dry-run', 'diff --check', 'git status', 'git log', 'select-string', 'get-content', 'python scripts/watcher/smoke']
if any(term in cmd for term in destructive_terms): level = 'destructive'
elif any(term in cmd for term in mutation_terms): level = 'mutating'
elif any(term in cmd for term in dry_terms): level = 'read_only_or_dry_run'
elif cmd.strip() == '': level = 'empty'
else: level = 'unknown_review_required'
payload = {'schema': 'ai_bridge_local.governance_risk_classifier', 'schema_version': 1, 'executes_commands': False, 'command_length': len(args.command), 'risk_level': level, 'destructive_hits': [term for term in destructive_terms if term in cmd], 'mutation_hits': [term for term in mutation_terms if term in cmd], 'dry_run_hits': [term for term in dry_terms if term in cmd]}
print(json.dumps(payload, ensure_ascii=False, indent=2))
