import pathlib

probe = pathlib.Path('scripts/watcher/command_status_probe.py').read_text(encoding='utf-8')
doc = pathlib.Path('docs/COMMAND_STATUS_PROBE.md').read_text(encoding='utf-8')

assert 'COMMAND_STATUS_PROBE_START' in probe
assert 'COMMAND_STATUS_PROBE_END' in probe
assert 'command_id' in probe
assert 'queue_local.db' in probe or 'DB_PATH' in probe
assert 'command_id' in doc
assert 'result_is_final=1' in doc
assert 'script_text' in doc

print('OK smoke_command_status_probe')
