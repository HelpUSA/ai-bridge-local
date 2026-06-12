# -- coding: utf-8 --
from pathlib import Path
ROOT = Path.cwd()
cs = (ROOT / 'extension/content_script.js').read_text(encoding='utf-8')
gw = (ROOT / 'gateway_local.py').read_text(encoding='utf-8')
wk = (ROOT / 'brain_worker.py').read_text(encoding='utf-8')
assert '@@AI_BRIDGE_LOCAL_START@@' in cs and '@@AI_BRIDGE_LOCAL_END@@' in cs
print('OK content_script_has_markers')
needle = '@@AI_BRIDGE_LOCAL_START@@[ ' + chr(92) + 't]*(?:' + chr(92) + 'r?' + chr(92) + 'n)?'
assert needle in cs
print('OK single_line_envelope_regex')
assert 'inter_agent_message' in gw
print('OK gateway_inter_agent_message')
assert 'local_capability' in gw
print('OK gateway_local_capability')
assert 'invalid_messages' in gw and 'record_invalid_message' in gw
print('OK gateway_invalid_messages')
assert 'dead_letters' in gw and 'record_dead_letter' in gw
print('OK gateway_dead_letters')
assert 'def prepare_temp_script' in wk
print('OK worker_prepare_temp_script')
assert 'script_text' in wk
print('OK worker_script_text')
assert 'script_ext' in wk
print('OK worker_script_ext')
assert 'timeout_seconds' in wk
print('OK worker_timeout_seconds')
print('ROBUSTNESS_SMOKE_OK')
import py_compile
diag_path = ROOT / 'scripts' / 'watcher' / 'control_center_diagnostics.py'
assert diag_path.exists()
py_compile.compile(str(diag_path), doraise=True)
diag = diag_path.read_text(encoding='utf-8')
assert 'AI_BRIDGE_LOCAL_DIAGNOSTICS' in diag
assert 'invalid_messages' in diag
assert 'dead_letters' in diag
assert 'where status=?' in diag
print('OK diagnostics_report')
cmd_smoke = ROOT / 'scripts' / 'watcher' / 'smoke_command_builder.py'
assert cmd_smoke.exists()
print('OK command_builder_smoke_present')
