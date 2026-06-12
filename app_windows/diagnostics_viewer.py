import subprocess, sys, tkinter as tk
from pathlib import Path
ROOT = Path.cwd()
CREATE_NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
def run_report():
 cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'control_center_diagnostics.py')]
 proc = subprocess.run(cmd, cwd=str(ROOT), text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30, creationflags=CREATE_NO_WINDOW)
 out = proc.stdout or ''
 if proc.stderr: out += chr(10) + 'STDERR:' + chr(10) + proc.stderr
 return out
def refresh():
 text.config(state='normal')
 text.delete('1.0', tk.END)
 try: text.insert(tk.END, run_report() or 'Sem saida de diagnostico.')
 except Exception as exc: text.insert(tk.END, 'Erro ao executar diagnostico: ' + str(exc))
 text.config(state='disabled')
root = tk.Tk()
root.title('AI Bridge Local - Diagnosticos')
root.geometry('980x620')
bar = tk.Frame(root)
bar.pack(fill='x')
tk.Button(bar, text='Atualizar', command=refresh).pack(side='left', padx=6, pady=6)
text = tk.Text(root, wrap='none')
text.pack(fill='both', expand=True)
refresh()
root.mainloop()
