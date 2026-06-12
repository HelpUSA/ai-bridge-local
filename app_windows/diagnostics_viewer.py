import subprocess, sys, tkinter as tk
from pathlib import Path
ROOT = Path.cwd()
CREATE_NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
def run_report(limit='10', target='gateway-brain-supervisor', prefix='ai_bridge_local'):
 cmd = [sys.executable, str(ROOT / 'scripts' / 'watcher' / 'control_center_diagnostics.py'), '--limit', str(limit), '--target', target, '--command-prefix', prefix]
 proc = subprocess.run(cmd, cwd=str(ROOT), text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=30, creationflags=CREATE_NO_WINDOW)
 out = proc.stdout or ''
 if proc.stderr: out += chr(10) + 'STDERR:' + chr(10) + proc.stderr
 return out
def refresh():
 text.config(state='normal')
 text.delete('1.0', tk.END)
 try: text.insert(tk.END, run_report(limit_var.get(), target_var.get(), prefix_var.get()) or 'Sem saida de diagnostico.')
 except Exception as exc: text.insert(tk.END, 'Erro ao executar diagnostico: ' + str(exc))
 text.config(state='disabled')
def copy_report():
 root.clipboard_clear()
 root.clipboard_append(text.get('1.0', tk.END))
root = tk.Tk()
root.title('AI Bridge Local - Diagnosticos')
root.geometry('1040x660')
bar = tk.Frame(root)
bar.pack(fill='x')
limit_var = tk.StringVar(value='10')
target_var = tk.StringVar(value='gateway-brain-supervisor')
prefix_var = tk.StringVar(value='ai_bridge_local')
tk.Label(bar, text='Limit').pack(side='left', padx=(6,2), pady=6)
tk.Entry(bar, textvariable=limit_var, width=6).pack(side='left', padx=2, pady=6)
tk.Label(bar, text='Target').pack(side='left', padx=(6,2), pady=6)
tk.Entry(bar, textvariable=target_var, width=28).pack(side='left', padx=2, pady=6)
tk.Label(bar, text='Prefix').pack(side='left', padx=(6,2), pady=6)
tk.Entry(bar, textvariable=prefix_var, width=24).pack(side='left', padx=2, pady=6)
tk.Button(bar, text='Atualizar', command=refresh).pack(side='left', padx=6, pady=6)
tk.Button(bar, text='Copiar', command=copy_report).pack(side='left', padx=6, pady=6)
text = tk.Text(root, wrap='none')
text.pack(fill='both', expand=True)
refresh()
root.mainloop()
