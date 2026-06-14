import argparse
import json
parser = argparse.ArgumentParser(description='Build a safe non-executing operational plan.')
parser.add_argument('--objective', required=True)
parser.add_argument('--repo', default='.')
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
objective = args.objective.strip()
if not objective: raise SystemExit('objective is required')
phases = [{'name': 'inspect', 'action': 'read git status, latest commits, roadmap, and relevant files', 'gate': 'no changes allowed'}, {'name': 'plan', 'action': 'propose smallest safe patch and validation list', 'gate': 'requires explicit approval before execution'}, {'name': 'execute', 'action': 'run only approved commands with validations between phases', 'gate': 'stop on first failure'}, {'name': 'audit', 'action': 'verify status, tests, docs, tag, and push state', 'gate': 'repo must finish clean or report exact pending state'}]
payload = {'schema': 'ai_bridge_local.planner_mode', 'schema_version': 1, 'objective': objective, 'repo': args.repo, 'executes_commands': False, 'requires_approval': True, 'phases': phases}
if args.json: print(json.dumps(payload, ensure_ascii=False, indent=2)); raise SystemExit(0)
lines = ['AI_BRIDGE_LOCAL_PLAN', 'Objective: ' + objective, 'Repo: ' + args.repo, 'Executes commands: no', 'Requires approval: yes', '']
[lines.extend([phase['name'].upper(), '- action: ' + phase['action'], '- gate: ' + phase['gate'], '']) for phase in phases]
print(chr(10).join(lines))
