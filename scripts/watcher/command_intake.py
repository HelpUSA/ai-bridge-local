import argparse
import json
import os
import subprocess
import time

CATALOG = {
	'inspect_repo': {'risk': 'read_only', 'steps': [['git', 'status', '-sb'], ['git', 'log', '--oneline', '--decorate', '-5']]},
	'inspect_docs': {'risk': 'read_only', 'steps': [['git', 'status', '-sb'], ['python', 'scripts/watcher/smoke_docs.py']]},
	'run_smokes': {'risk': 'validation', 'steps': [['python', 'scripts/watcher/smoke_version_alignment.py'], ['python', 'scripts/watcher/smoke_command_builder_validate.py'], ['python', 'scripts/watcher/smoke_docs.py']]},
	'run_release_check': {'risk': 'validation', 'steps': [['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/watcher/release_check.ps1']]},
 'validate_release': {'risk': 'validation', 'steps': [['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/watcher/release_check.ps1']]},
	'diagnose_failure': {'risk': 'read_only', 'steps': [['python', 'scripts/watcher/post_failure_triage.py']]},
	'inspect_delivery_failure': {'risk': 'read_only', 'steps': [['python', 'scripts/watcher/inspect_delivery_failure.py', '--limit', '5']]},
	'backup_queue': {'risk': 'read_only', 'steps': [['python', 'scripts/watcher/backup_queue_db.py']]},
	'cleanup_plan': {'risk': 'read_only', 'steps': [['python', 'scripts/watcher/cleanup_plan.py']]},
	'apply_patch_file': {'risk': 'write_file', 'steps': []},
	'bump_version': {'risk': 'git_write', 'steps': []},
	'commit_and_tag': {'risk': 'git_write', 'steps': []},
	'push_release': {'risk': 'network_push', 'steps': []},
}

RISK_POLICY = {
	'read_only': 'execute directly',
	'validation': 'execute with timeout',
	'write_file': 'require clean repo and planned file list',
	'git_write': 'require smokes and release_check',
	'destructive': 'require dry-run and explicit acknowledgement',
	'network_push': 'require successful release_check',
}

DESTRUCTIVE_TOKENS = ['remove-item', ' rm ', ' del ', ' rmdir ', 'git reset', 'git clean', 'erase ']
MAX_INLINE_COMMAND = 500
MAX_TIMEOUT = 600

def check_inline_command(text, dry_run):
	if not text:
		return
	low = (' ' + text.lower() + ' ')
	if len(text) > MAX_INLINE_COMMAND:
		raise SystemExit('inline command too large')
	if 'AI_BRIDGE_LOCAL_START' in text or 'AI_BRIDGE_LOCAL_END' in text:
		raise SystemExit('inline command contains watcher marker')
	if any(token in low for token in DESTRUCTIVE_TOKENS) and not dry_run:
		raise SystemExit('destructive command requires dry-run')

def build_plan(intent, cwd, command_id, timeout, dry_run, allow_git_write, allow_network_push, release_check_ok, inline_command, subject_command_id=''):
	if intent not in CATALOG:
		raise SystemExit('unknown intent: ' + intent)
	if timeout < 1 or timeout > MAX_TIMEOUT:
		raise SystemExit('timeout outside policy')
	abs_cwd = os.path.abspath(cwd)
	if not os.path.isdir(abs_cwd):
		raise SystemExit('cwd does not exist: ' + cwd)
	check_inline_command(inline_command, dry_run)
	item = CATALOG[intent]
	risk = item['risk']
	if risk == 'git_write' and not allow_git_write:
		raise SystemExit('git_write requires allow-git-write')
	if risk == 'network_push' and (not allow_network_push or not release_check_ok):
		raise SystemExit('network_push requires allow-network-push and release-check-ok')
	if intent == 'inspect_delivery_failure' and subject_command_id:
		item_steps = [['python', 'scripts/watcher/inspect_delivery_failure.py', '--command-id', subject_command_id]]
	else:
		item_steps = item['steps']
	steps = []
	for index, command in enumerate(item_steps, 1):
		steps.append({'index': index, 'type': 'run', 'command': command})
	return {'schema': 'ai_bridge_local.command_intake_plan', 'schema_version': 2, 'command_id': command_id, 'intent': intent, 'cwd': abs_cwd, 'risk': risk, 'risk_policy': RISK_POLICY[risk], 'status': 'planned', 'dry_run': dry_run, 'steps': steps}

def execute_plan(plan, timeout):
	if plan['risk'] not in {'read_only', 'validation'}:
		raise SystemExit('execution blocked for risk: ' + plan['risk'])
	results = []
	status = 'acked'
	for step in plan['steps']:
		cp = subprocess.run(step['command'], cwd=plan['cwd'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
		results.append({'index': step['index'], 'command': step['command'], 'return_code': cp.returncode, 'stdout_tail': cp.stdout[-2000:], 'stderr_tail': cp.stderr[-2000:]})
		if cp.returncode != 0:
			status = 'failed'
			break
	out = dict(plan)
	out['status'] = status
	out['results'] = results
	return out

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--intent', required=True)
	parser.add_argument('--cwd', default='.')
	parser.add_argument('--command-id', default='intake_' + str(int(time.time())))
	parser.add_argument('--execute', action='store_true')
	parser.add_argument('--timeout', type=int, default=120)
	parser.add_argument('--dry-run', action='store_true')
	parser.add_argument('--allow-git-write', action='store_true')
	parser.add_argument('--allow-network-push', action='store_true')
	parser.add_argument('--release-check-ok', action='store_true')
	parser.add_argument('--inline-command', default='')
	parser.add_argument('--subject-command-id', default='')
	args = parser.parse_args()
	plan = build_plan(args.intent, args.cwd, args.command_id, args.timeout, args.dry_run, args.allow_git_write, args.allow_network_push, args.release_check_ok, args.inline_command, args.subject_command_id)
	if args.execute:
		plan = execute_plan(plan, args.timeout)
	print(json.dumps(plan, indent=2, sort_keys=True))
	return 0 if plan['status'] in {'planned', 'acked'} else 1

if __name__ == '__main__':
	raise SystemExit(main())
