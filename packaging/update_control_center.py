import subprocess
import sys
import time
import shutil
from pathlib import Path
ROOT = Path.cwd()
NAME = 'AI-Bridge-Local-Control-Center'
EXE = ROOT / 'dist' / NAME / (NAME + '.exe')
time.sleep(2)
base = Path(sys.base_prefix) / 'tcl'
tcl = base / 'tcl8.6'
tk = base / 'tk8.6'
subprocess.run(['taskkill','/IM', NAME + '.exe','/F'], check=False)
shutil.rmtree(ROOT / 'build' / NAME, ignore_errors=True)
shutil.rmtree(ROOT / 'dist' / NAME, ignore_errors=True)
cmd = [sys.executable,'-m','PyInstaller','--noconfirm','--clean','--onedir','--windowed','--name',NAME] + ['--hidden-import', 'tkinter', '--hidden-import', 'tkinter.ttk', '--hidden-import', 'tkinter.messagebox', '--hidden-import', '_tkinter', '--collect-submodules', 'tkinter'] + ['--add-data',str(tcl)+';_tcl_data','--add-data',str(tk)+';_tk_data','--add-data',str(tcl)+';tcl','--add-data',str(tk)+';tk','app_windows/control_center_app.py']
subprocess.run(cmd, check=True, cwd=str(ROOT))
subprocess.Popen([str(EXE)], cwd=str(ROOT))
