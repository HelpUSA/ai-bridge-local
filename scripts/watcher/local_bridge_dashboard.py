import argparse
import json
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Read-only dashboard for local bridge store.')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
parser.add_argument('--limit', type=int, default=5)
args = parser.parse_args()
store = Path(args.store_dir)
store = store if store.is_absolute() else ROOT / store
store = store.resolve()
names = ['inbox', 'outbox', 'status']
files = {name: store / (name + '.jsonl') for name in names}
lines = {name: (files[name].read_text(encoding='utf-8').splitlines() if files[name].exists() else []) for name in names}
counts = {name: len(lines[name]) for name in names}
recent = {name: lines[name][-args.limit:] for name in names}
payload = {'schema': 'ai_bridge_local.local_bridge_dashboard', 'schema_version': 1, 'executes_commands': False, 'store_dir': str(store), 'counts': counts, 'recent' : recent, 'health': 'ok' if sum(counts.values()) >= 0 else 'unknown'}
print(json.dumps(payload, ensure_ascii=False, indent=2))
