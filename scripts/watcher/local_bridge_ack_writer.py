import argparse
import json
import time
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Plan or write local bridge ack status records.')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
parser.add_argument('--message-id', default='preview-message-id')
parser.add_argument('--status', choices=['acked', 'failed', 'delivering'], default='acked')
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
store = Path(args.store_dir)
store = store if store.is_absolute() else ROOT / store
store = store.resolve()
allowed = str(store).startswith(str(ROOT))
record = {'id': args.message_id, 'status': args.status, 'created_at_epoch': int(time.time()), 'source': 'local_bridge_ack_writer'}
if args.apply and allowed:
 store.mkdir(parents=True, exist_ok=True)
 with (store / 'status.jsonl').open('a', encoding='utf-8') as fh: fh.write(json.dumps(record, ensure_ascii=False) + chr(10))
payload = {'schema': 'ai_bridge_local.local_bridge_ack_writer', 'schema_version': 1, 'executes_commands': False, 'dry_run': not args.apply, 'allowed': allowed, 'store_dir': str(store), 'record': record}
print(json.dumps(payload, ensure_ascii=False, indent=2))
