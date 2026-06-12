import json
from pathlib import Path
ROOT = Path.cwd()
EXAMPLES = ROOT / 'examples'
required = ['command_id', 'source_chat_id', 'target_chat_id', 'action', 'delivery_kind', 'conversation_id', 'payload']
for path in sorted(EXAMPLES.glob('.txt')):
	lines = path.read_text(encoding='utf-8-sig').splitlines()
	assert lines[0].strip() == '@@AI_BRIDGE_LOCAL_START@@', path
	assert lines[-1].strip() == '@@AI_BRIDGE_LOCAL_END@@', path
	body = chr(10).join(lines[1:-1]).strip()
	data = json.loads(body)
	for key in required: assert key in data, (path, key)
	assert isinstance(data['payload'], dict), path
	if path.name.startswith('run_'):
		assert 'cwd' in data['payload'], path
		assert 'command' in data['payload'], path
print('OK examples_smoke')
