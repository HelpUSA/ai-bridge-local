import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Build local envelope with non-blocking governance advisory metadata.')
parser.add_argument('--source', required=True)
parser.add_argument('--target', required=True)
parser.add_argument('--action', choices=['send-chat-message', 'run-command'], required=True)
parser.add_argument('--id', default='local_advisory_envelope')
parser.add_argument('--message', default='')
parser.add_argument('--cwd', default='.')
parser.add_argument('--timeout', type=int, default=300)
parser.add_argument('--output-file', default='')
parser.add_argument('--command', nargs=argparse.REMAINDER, default=[])
args = parser.parse_args()
env = {'command_id': args.id, 'source_chat_id': args.source, 'target_chat_id': args.target, 'action': args.action}
if args.action == 'send-chat-message':
 env['delivery_kind'] = 'inter_agent_message'
 env['message'] = args.message
 env['governance_advisory'] = {'schema': 'ai_bridge_local.governance_advisory', 'schema_version': 1, 'executes_commands': False, 'blocks_execution': False, 'risk_level': 'message_only', 'requires_manual_review': False, 'warnings': []}
if args.action == 'run-command':
 command_value = args.command if args.command else ['git', 'status', '-sb']
 command_text = ' '.join(command_value)
 preflight = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'watcher' / 'governance_preflight.py'), '--command', command_text], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
 env['delivery_kind'] = 'local_capability'
 env['payload'] = {'cwd': args.cwd, 'timeout_seconds': args.timeout, 'command': command_value, 'governance_advisory': json.loads(preflight.stdout)}
out = '@@AI_BRIDGE_LOCAL_START@@' + chr(10) + json.dumps(env, ensure_ascii=False, separators=(',', ':')) + chr(10) + '@@AI_BRIDGE_LOCAL_END@@' + chr(10)
if args.output_file:
 Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
 Path(args.output_file).write_text(out, encoding='utf-8')
else:
 print(out, end='')
