import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Build envelope and optionally enqueue it into local bridge store.')
parser.add_argument('--from-chat', default='local-source')
parser.add_argument('--to-chat', default='local-target')
parser.add_argument('--message', default='hello local writer')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
env_cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_envelope.py'), '--from-chat', args.from_chat, '--to-chat', args.to_chat, '--message', args.message]
env = subprocess.run(env_cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
envelope = json.loads(env.stdout)
store_cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_store.py'), '--store-dir', args.store_dir, '--action', 'enqueue', '--box', 'outbox', '--message', json.dumps(envelope, ensure_ascii=False)]
if args.apply: store_cmd.append('--apply')
stored = subprocess.run(store_cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
payload = {'schema': 'ai_bridge_local.local_bridge_writer', 'schema_version': 1, 'executes_commands': False, 'dry_run': not args.apply, 'envelope_valid': envelope.get('valid', False), 'target_chat_id': envelope.get('target_chat_id', ''), 'store_result': json.loads(stored.stdout)}
print(json.dumps(payload, ensure_ascii=False, indent=2))
