from pathlib import Path
ROOT = Path.cwd()
viewer = ROOT / 'app_windows' / 'diagnostics_viewer.py'
launcher = ROOT / 'app_windows' / 'start_diagnostics_viewer.ps1'
assert viewer.exists(), viewer
assert launcher.exists(), launcher
v = viewer.read_text(encoding='utf-8')
s = launcher.read_text(encoding='utf-8')
assert 'control_center_diagnostics.py' in v
assert 'def run_report' in v
assert 'def refresh' in v
assert 'python app_windows/diagnostics_viewer.py' in s
print('OK diagnostics_viewer_smoke')
