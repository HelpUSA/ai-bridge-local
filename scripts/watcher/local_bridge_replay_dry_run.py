import argparse
import json
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Dry-run replay planner for local bridge envelopes.')
parser.add_argument('--envelope-file', default='')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
store = Path(args.store_dir)
store = store if store.is_absolute() else ROOT / store
store = store.resolve()
envelope = json.loads(Path(args.envelope_file).read_text(encoding='utf-8')) if args.envelope_file else {'schema': 'ai_bridge_local.local_bridge_envelope', 'valid': True, 'message': 'preview'}
plan = ['load envelope', 'validate root message field', 'append to outbox when apply is approved', 'emit queued status', 'wait for receiver ack']
payload = {'schema': 'ai_bridge_local.local_bridge_replay_plan', 'schema_version': 1, 'executes_commands': False, 'dry_run': not args.apply, 'store_dir': str(store), 'envelope_valid': bool(envelope.get('valid', False)), 'target_chat_id': envelope.get('target_chat_id', ''), 'plan': plan}
print(json.dumps(payload, ensure_ascii=False, indent=2))
