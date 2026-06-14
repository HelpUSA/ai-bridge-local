from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))
from brain_worker import execute_command

result = execute_command({'cwd': '.', 'timeout_seconds': 120, 'intent': 'inspect_repo'}, 'smoke_intent_payload')
assert result['return_code'] == 0, result
assert 'inspect_repo' in result['stdout'], result['stdout']
assert 'ai_bridge_local.command_intake_plan' in result['stdout'], result['stdout']

executed = execute_command({'cwd': '.', 'timeout_seconds': 120, 'intent': 'run_smokes', 'execute_intent': True}, 'smoke_intent_payload_execute')
assert executed['return_code'] == 0, executed
assert 'acked' in executed['stdout'], executed['stdout']
print('OK intent_payload_smoke')
