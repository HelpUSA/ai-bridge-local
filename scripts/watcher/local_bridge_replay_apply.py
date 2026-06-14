import argparse
import json
import time
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Controlled local bridge replay with dry-run default.')
parser.add_argument('--envelope-file', default='')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
store = Path(args.store_dir)
store = store if store.is_absolute() else ROOT / store
store = store.resolve()
allowed = str(store).startswith(str(ROOT))
envelope = json.loads(Path(args.envelope_file).read_text(encoding='utf-8')) if args.envelope_file else {'schema': 'ai_bridge_local.local_bridge_envelope', 'valid': True, 'id': 'preview', 'target_chat_id': 'preview-target', 'message': 'preview'}
valid = bool(envelope.get('valid', False)) and 'message' in envelope and bool(envelope.get('target_chat_id', ''))
record = {'id': envelope.get('id', 'preview'), 'status': 'queued', 'target_chat_id': envelope.get('target_chat_id', ''), 'created_at_epoch': int(time.time()), 'envelope': envelope}
if args.apply and allowed and valid:
 store.mkdir(parents=True, exist_ok=True)
 with (store / 'outbox.jsonl').open('a', encoding='utf-8') as fh: fh.write(json.dumps(record, ensure_ascii=False) + chr(10))
 with (store / 'status.jsonl').open('a', encoding='utf-8') as fh: fh.write(json.dumps({'id': record['id'], 'status': 'queued', 'source': 'local_bridge_replay_apply'}, ensure_ascii=False) + chr(10))
outbox_count = len((store / 'outbox.jsonl').read_text(encoding='utf-8').splitlines()) if (store / 'outbox.jsonl').exists() else 0
payload = {'schema': 'ai_bridge_local.local_bridge_replay_apply', 'schema_version': 1, 'executes_commands': False, 'dry_run': not args.apply, 'allowed': allowed, 'valid_envelope': valid, 'store_dir': str(store), 'outbox_count': outbox_count, 'planned_or_written_record': record}
print(json.dumps(payload, ensure_ascii=False, indent=2))
