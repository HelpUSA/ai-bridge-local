from future import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
STATE_DIR = ROOT / 'runtime' / 'smart_tasks'
STATE = STATE_DIR / 'smoke_smart_task.json'
NOTES_DIR = ROOT / 'knowledge' / 'tasks'


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
 return subprocess.run(
 args,
 cwd=ROOT,
 check=True,
 text=True,
 encoding='utf-8',
 errors='replace',
 stdout=subprocess.PIPE,
 stderr=subprocess.PIPE,
 )


def cleanup() -> None:
 if STATE.exists():
 STATE.unlink()
 if NOTES_DIR.exists():
 for path in NOTES_DIR.glob('smart-task-smoke*'):
 path.unlink()
 if STATE_DIR.exists() and not any(STATE_DIR.iterdir()):
 STATE_DIR.rmdir()


cleanup()

run(['python', 'scripts/watcher/smart_task_runner.py', 'demo', '--task-id', 'smoke_smart_task', '--dry-run', '--print-state'])
payload = json.loads(STATE.read_text(encoding='utf-8'))
assert payload['task_id'] == 'smoke_smart_task'
assert payload['status'] == 'dry_run'
notes = list(NOTES_DIR.glob('smart-task-smoke*'))
assert notes, 'knowledge note was not created'
note_text = notes[0].read_text(encoding='utf-8')
assert 'Demonstrar execucao' in note_text
assert 'dry_run' in note_text
assert 'inspect' in note_text

cleanup()

run(['python', 'scripts/watcher/smart_task_runner.py', 'demo', '--task-id', 'smoke_smart_task', '--dry-run', '--print-state', '--no-knowledge'])
payload = json.loads(STATE.read_text(encoding='utf-8'))
assert payload['task_id'] == 'smoke_smart_task'
assert payload['status'] == 'dry_run'
assert not list(NOTES_DIR.glob('smart-task-smoke*')), '--no-knowledge created note'

cleanup()

print('OK smoke_smart_task_runner')
