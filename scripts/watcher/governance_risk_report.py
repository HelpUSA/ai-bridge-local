import argparse
import json
from collections import Counter
from pathlib import Path
parser = argparse.ArgumentParser(description='Summarize governance decision JSONL logs.')
parser.add_argument('--log-file', default='reports/governance_decisions.jsonl')
args = parser.parse_args()
log_path = Path(args.log_file)
items = []
if log_path.exists():
 items = [json.loads(x) for x in log_path.read_text(encoding='utf-8').splitlines() if x.strip()]
counts = Counter(x.get('risk_level', 'unknown') for x in items)
manual = sum(1 for x in items if x.get('requires_manual_review'))
payload = {'schema': 'ai_bridge_local.governance_risk_report', 'schema_version': 1, 'total': len(items), 'requires_manual_review': manual, 'risk_counts': dict(sorted(counts.items())), 'source_log': str(log_path)}
print(json.dumps(payload, ensure_ascii=False, indent=2))
