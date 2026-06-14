import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Read-only governance preflight for watcher commands.')
parser.add_argument('--command', default='')
parser.add_argument('--allow-mutating', action='store_true')
parser.add_argument('--allow-destructive', action='store_true')
args = parser.parse_args()
classifier = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_risk_classifier.py'), '--command', args.command], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
risk = json.loads(classifier.stdout)
level = risk.get('risk_level', 'unknown_review_required')
warnings = []
if level == 'mutating' and not args.allow_mutating: warnings.append('mutating command requires explicit review flag')
if level == 'destructive' and not args.allow_destructive: warnings.append('destructive command requires explicit review flag')
if level == 'unknown_review_required': warnings.append('unknown command requires manual review')
payload = {'schema': 'ai_bridge_local.governance_preflight', 'schema_version': 1, 'executes_commands': False, 'blocks_execution': False, 'risk_level': level, 'requires_manual_review': len(warnings) > 0, 'warnings': warnings, 'classifier': risk}
print(json.dumps(payload, ensure_ascii=False, indent=2))
