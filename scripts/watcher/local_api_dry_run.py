import argparse
import json
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Dry-run local API planner for future file and command operations.')
parser.add_argument('--intent', default='read_status')
parser.add_argument('--path', default='VERSION')
parser.add_argument('--command', default='git status -sb')
args = parser.parse_args()
rel = Path(args.path)
target = (ROOT / rel).resolve()
allowed_path = str(target).startswith(str(ROOT))
allowed_intents = ['read_status', 'read_file', 'write_file_dry_run', 'run_command_dry_run']
payload = {'schema': 'ai_bridge_local.local_api_dry_run', 'schema_version': 1, 'executes_commands': False, 'intent': args.intent, 'intent_allowed': args.intent in allowed_intents, 'path': args.path, 'path_allowed': allowed_path, 'command': args.command, 'planned_actions': ['validate intent', 'validate path', 'return plan only', 'require explicit approval before mutation or execution']}
print(json.dumps(payload, ensure_ascii=False, indent=2))
