import argparse
import json
SCHEMA = 'ai_bridge_local.handoff_template'
SCHEMA_VERSION = 1
parser = argparse.ArgumentParser(description='Build a safe handoff summary between watcher chats.')
parser.add_argument('--project', required=True)
parser.add_argument('--repo', required=True)
parser.add_argument('--status', required=True)
parser.add_argument('--files', default='')
parser.add_argument('--validations', default='')
parser.add_argument('--pending', default='none')
parser.add_argument('--next-command', required=True)
parser.add_argument('--json', action='store_true')
args = parser.parse_args()
files_changed = [item.strip() for item in args.files.split(',') if item.strip()]
validations = [item.strip() for item in args.validations.split(',') if item.strip()]
data = {'schema': SCHEMA, 'schema_version': SCHEMA_VERSION, 'project': args.project.strip(), 'repo': args.repo.strip(), 'status': args.status.strip(), 'files_changed': files_changed, 'validations': validations, 'pending': args.pending.strip(), 'next_safe_command': args.next_command.strip()}
missing = [key for key in ['project', 'repo', 'status', 'next_safe_command'] if not data[key]]
if missing: raise SystemExit('missing required handoff fields: ' + ', '.join(missing))
if args.json: print(json.dumps(data, ensure_ascii=False, indent=2)); raise SystemExit(0)
files = data['files_changed'] or ['none']
vals = data['validations'] or ['none']
lines = ['AI_BRIDGE_LOCAL_HANDOFF', '', 'Project: ' + data['project'], 'Repo: ' + data['repo'], '', 'Current status:', '- ' + data['status'], '', 'Files changed:'] + ['- ' + item for item in files] + ['', 'Validations:'] + ['- ' + item for item in vals] + ['', 'Pending:', '- ' + (data['pending'] or 'none'), '', 'Next safe command:', data['next_safe_command']]
print(chr(10).join(lines))
