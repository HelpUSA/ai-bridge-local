import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
BUILDER = ROOT / 'scripts' / 'watcher' / 'command_builder.py'
VALIDATOR = ROOT / 'scripts' / 'watcher' / 'envelope_validator.py'

def build(args):
 return subprocess.check_output([sys.executable, str(BUILDER)] + args, cwd=ROOT, text=True, encoding='utf-8')

def validate(raw):
 proc = subprocess.run([sys.executable, str(VALIDATOR)], input=raw, cwd=ROOT, text=True, encoding='utf-8', capture_output=True)
 assert proc.returncode == 0, proc.stdout + proc.stderr
 assert 'VALID' in proc.stdout, proc.stdout

def parse_envelope(raw):
 kept = [line for line in raw.splitlines() if not line.startswith(chr(64) + chr(64) + 'AI_BRIDGE_LOCAL_')]
 return json.loads(chr(10).join(kept))

raw = build([
 '--id', 'smoke-send-chat-message',
 '--source', 'source-chat',
 '--target', 'target-chat',
 '--action', 'send-chat-message',
 '--message', 'hello from send chat smoke',
])
validate(raw)
env = parse_envelope(raw)
assert env['schema'] == 'ai_bridge_local.envelope', env
assert env['schema_version'] == 1, env
assert env['command_id'] == 'smoke-send-chat-message', env
assert env['source_chat_id'] == 'source-chat', env
assert env['target_chat_id'] == 'target-chat', env
assert env['action'] == 'send-chat-message', env
assert env['delivery_kind'] == 'inter_agent_message', env
assert env['message'] == 'hello from send chat smoke', env
assert 'payload' not in env, env

missing = subprocess.run([
 sys.executable, str(BUILDER),
 '--id', 'smoke-send-chat-message-missing',
 '--source', 'source-chat',
 '--target', 'target-chat',
 '--action', 'send-chat-message',
], cwd=ROOT, text=True, encoding='utf-8', capture_output=True)
assert missing.returncode != 0, missing.stdout + missing.stderr
assert 'message required' in (missing.stdout + missing.stderr), missing.stdout + missing.stderr

print('OK send_chat_message_smoke')
