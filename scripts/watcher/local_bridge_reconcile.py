import argparse
import json
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Read-only local bridge status reconciler.')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
args = parser.parse_args()
store_dir = Path(args.store_dir)
store_dir = store_dir if store_dir.is_absolute() else ROOT / store_dir
store_dir = store_dir.resolve()
files = {name: store_dir / (name + '.jsonl') for name in ['inbox', 'outbox', 'status']}
counts = {name: (len(path.read_text(encoding='utf-8').splitlines()) if path.exists() else 0) for name, path in files.items()}
payload = {'schema': 'ai_bridge_local.local_bridge_reconcile', 'schema_version': 1, 'executes_commands': False, 'store_dir': str(store_dir), 'counts': counts, 'recommendation': 'review counts before any cleanup or replay'}
print(json.dumps(payload, ensure_ascii=False, indent=2))
