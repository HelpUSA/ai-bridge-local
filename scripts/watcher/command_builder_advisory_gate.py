import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Optional non-default gate for command_builder_advisory.')
parser.add_argument('--fail-on-mutating', action='store_true')
parser.add_argument('--fail-on-destructive', action='store_true')
parser.add_argument('--source', required=True)
parser.add_argument('--target', required=True)
parser.add_argument('--action', choices=['send-chat-message', 'run-command'], required=True)
parser.add_argument('--id', default='local_advisory_gate_envelope')
parser.add_argument('--message', default='')
parser.add_argument('--cwd', default='.')
parser.add_argument('--timeout', type=int, default=300)
parser.add_argument('--output-file', default='')
parser.add_argument('--command', nargs=argparse.REMAINDER, default=[])
args = parser.parse_args()
tmp = Path(tempfile.mkdtemp()) / 'gate_envelope.txt'
cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'command_builder_advisory.py'), '--source', args.source, '--target', args.target, '--action', args.action, '--id', args.id, '--cwd', args.cwd, '--timeout', str(args.timeout), '--output-file', str(tmp)]
if args.action == 'send-chat-message':
 cmd = cmd + ['--message', args.message]
if args.action == 'run-command':
 cmd = cmd + ['--command'] + (args.command if args.command else ['git', 'status', '-sb'])
subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
raw = tmp.read_text(encoding='utf-8')
body = raw.split('@@AI_BRIDGE_LOCAL_START@@', 1)[1].split('@@AI_BRIDGE_LOCAL_END@@', 1)[0].strip()
env = json.loads(body)
adv = env.get('payload', {}).get('governance_advisory', env.get('governance_advisory', {}))
level = adv.get('risk_level', 'unknown_review_required')
blocked = (args.fail_on_destructive and level == 'destructive') or (args.fail_on_mutating and level in ['mutating', 'destructive'])
if blocked:
 print(json.dumps({'schema': 'ai_bridge_local.governance_optional_gate', 'schema_version': 1, 'blocks_execution': True, 'risk_level': level, 'reason': 'optional gate flag requested failure'}, ensure_ascii=False, indent=2))
 raise SystemExit(40)
if args.output_file:
 Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
 Path(args.output_file).write_text(raw, encoding='utf-8')
else:
 print(raw, end='')
