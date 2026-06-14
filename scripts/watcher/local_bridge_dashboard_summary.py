import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Text summary for local bridge dashboard.')
parser.add_argument('--store-dir', default='runtime/local_bridge_store')
args = parser.parse_args()
run = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'local_bridge_dashboard.py'), '--store-dir', args.store_dir], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
data = json.loads(run.stdout)
lines = ['AI_BRIDGE_LOCAL_BRIDGE_DASHBOARD', 'Store: ' + data['store_dir'], 'Inbox: ' + str(data['counts']['inbox']), 'Outbox: ' + str(data['counts']['outbox']), 'Status: ' + str(data['counts']['status']), 'Executes commands: no']
print(chr(10).join(lines))
