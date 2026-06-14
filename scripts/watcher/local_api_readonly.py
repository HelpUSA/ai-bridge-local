import argparse
import json
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Read-only local API probe for files and repo metadata.')
parser.add_argument('--path', default='VERSION')
parser.add_argument('--max-chars', type=int, default=1200)
args = parser.parse_args()
rel = Path(args.path)
target = (ROOT / rel).resolve()
allowed = str(target).startswith(str(ROOT))
exists = bool(allowed and target.exists())
is_file = bool(exists and target.is_file())
content = target.read_text(encoding='utf-8', errors='replace')[:args.max_chars] if is_file else ''
payload = {'schema': 'ai_bridge_local.local_api_readonly', 'schema_version': 1, 'executes_commands': False, 'repo': str(ROOT), 'requested_path': args.path, 'allowed': allowed, 'exists': exists, 'is_file': is_file, 'preview': content}
print(json.dumps(payload, ensure_ascii=False, indent=2))
