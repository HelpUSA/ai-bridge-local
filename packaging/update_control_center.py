import subprocess
import sys
import time
from pathlib import Path
ROOT = Path.cwd()
NAME = 'AI-Bridge-Local-Control-Center'
EXE = ROOT / 'dist' / NAME / (NAME + '.exe')
time.sleep(2)
subprocess.run([sys.executable, '-m', 'PyInstaller', '--clean', '--noconfirm', '--noconsole', '--name', NAME, 'app_windows/control_center_app.py'], cwd=str(ROOT), check=True)
subprocess.Popen([str(EXE)], cwd=str(ROOT))
