import argparse
import json
import time
import uuid
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Local inbox/outbox/status store with dry-run default.')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
parser.add_argument('--action', choices=['enqueue', 'list', 'status'], default='status')
parser.add_argument('--box', choices=['inbox', 'outbox'], default='outbox')
parser.add_argument('--message', default='hello from local bridge store')
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
store_dir = Path(args.store_dir)
store_dir = store_dir if store_dir.is_absolute() else ROOT / store_dir
store_dir = store_dir.resolve()
allowed = str(store_dir).startswith(str(ROOT)) or str(store_dir).startswith(str(Path.cwd().anchor))
box_file = store_dir / (args.box + '.jsonl')
status_file = store_dir / 'status.jsonl'
entry = {'id': str(uuid.uuid4()), 'created_at_epoch': int(time.time()), 'box': args.box, 'status': 'queued', 'message': args.message}
entries = box_file.read_text(encoding='utf-8').splitlines() if box_file.exists() else []
if args.action == 'enqueue' and args.apply and allowed:
 store_dir.mkdir(parents=True, exist_ok=True)
 with box_file.open('a', encoding='utf-8') as fh: fh.write(json.dumps(entry, ensure_ascii=False) + chr(10))
 with status_file.open('a', encoding='utf-8') as fh: fh.write(json.dumps({'id': entry['id'], 'status': 'queued', 'box': args.box}, ensure_ascii=False) + chr(10))
 entries = box_file.read_text(encoding='utf-8').splitlines() if box_file.exists() else []
payload = {'schema': 'ai_bridge_local.local_bridge_store', 'schema_version': 1, 'executes_commands': False, 'action': args.action, 'dry_run': not args.apply, 'store_dir': str(store_dir), 'allowed': allowed, 'box': args.box, 'entry_preview': entry, 'entry_count': len(entries), 'status_model': ['queued', 'acked', 'failed', 'delivering']}
print(json.dumps(payload, ensure_ascii=False, indent=2))
