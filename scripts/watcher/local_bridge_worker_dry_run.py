import argparse
import json
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Dry-run local bridge worker planner.')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
parser.add_argument('--limit', type=int, default=10)
args = parser.parse_args()
store = Path(args.store_dir)
store = store if store.is_absolute() else ROOT / store
store = store.resolve()
outbox = store / 'outbox.jsonl'
status_file = store / 'status.jsonl'
outbox_lines = outbox.read_text(encoding='utf-8').splitlines() if outbox.exists() else []
status_lines = status_file.read_text(encoding='utf-8').splitlines() if status_file.exists() else []
status_items = [json.loads(line) for line in status_lines if line.strip().startswith('{')]
status_by_id = {item.get('id', ''): item.get('status', '') for item in status_items}
outbox_items = [json.loads(line) for line in outbox_lines[-args.limit:] if line.strip().startswith('{')]
candidates = [{'id': item.get('id', ''), 'status': status_by_id.get(item.get('id', ''), 'queued'), 'target_chat_id': item.get('target_chat_id', ''), 'would_send': status_by_id.get(item.get('id', ''), 'queued') not in ['acked', 'failed']} for item in outbox_items]
payload = {'schema': 'ai_bridge_local.local_bridge_worker_dry_run', 'schema_version': 1, 'executes_commands': False, 'dry_run': True, 'store_dir': str(store), 'candidate_count': len(candidates), 'sendable_count': sum(1 for item in candidates if item['would_send']), 'candidates': candidates}
print(json.dumps(payload, ensure_ascii=False, indent=2))
