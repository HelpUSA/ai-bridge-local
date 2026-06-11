import os, sys
base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
extra = os.path.join(base, 'py_lib')
if os.path.isdir(extra) and extra not in sys.path:
    sys.path.insert(0, extra)
