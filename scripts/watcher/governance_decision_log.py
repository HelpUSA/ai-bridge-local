import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Append governance preflight decisions to JSONL log.')
parser.add_argument('--command-id', default='manual')
parser.add_argument('--log-file', default='reports/governance_decisions.jsonl')
parser.add_argument('--command', nargs=argparse.REMAINDER, default=[])
args = parser.parse_args()
command_value = args.command if args.command else ['git', 'status', '-sb']
command_text = ' '.join(command_value)
preflight = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_preflight.py'), '--command', command_text], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
advisory = json.loads(preflight.stdout)
event = {'schema': 'ai_bridge_local.governance_decision', 'schema_version': 1, 'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'command_id': args.command_id, 'command': command_value, 'risk_level': advisory.get('risk_level'), 'requires_manual_review': advisory.get('requires_manual_review'), 'warnings': advisory.get('warnings', []), 'advisory': advisory}
log_path = Path(args.log_file)
log_path.parent.mkdir(parents=True, exist_ok=True)
with log_path.open('a', encoding='utf-8') as f:
 f.write(json.dumps(event, ensure_ascii=False, separators=(',', ':')) + chr(10))
print(json.dumps(event, ensure_ascii=False, indent=2))
