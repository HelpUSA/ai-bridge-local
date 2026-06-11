# -- coding: utf-8 --
import json
import os
import shutil
import subprocess
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from urllib.request import urlopen

try:
	import psutil
except Exception:
	psutil = None

try:
	import pystray
	from PIL import Image, ImageDraw
	TRAY_AVAILABLE = True
except Exception:
	pystray = None
	Image = None
	ImageDraw = None
	TRAY_AVAILABLE = False

APP_VERSION = "14"
APP_TITLE = "AI Bridge Local - Central de Controle v14"
if getattr(sys, "frozen", False):
	ROOT = Path(sys.executable).resolve().parents[2]
else:
	ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:8766/control/status"
LOG_DIR = ROOT / "logs"
GATEWAY_LOG = LOG_DIR / "control_center_gateway.log"
WORKER_LOG = LOG_DIR / "control_center_worker.log"
MONITOR_LOG = LOG_DIR / "control_center_monitor.log"
LATEST_VERSION_FILE = ROOT / "app_windows" / "latest_version.txt"
UPDATE_LOG = LOG_DIR / "control_center_update.log"
PROCESS_KEYS = ["gateway_local.py", "brain_worker.py"]
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
DARK_BG = "#171717"
DARK_PANEL = "#242424"
DARK_PANEL_2 = "#333333"
DARK_TEXT = "#e5e7eb"
DARK_ACCENT = "#00a8e8"

def is_script_running(script_name):
	if psutil is None:
		return False
	for proc in psutil.process_iter(["pid", "cmdline"]):
		try:
			cmd = " ".join(proc.info.get("cmdline") or [])
			if script_name.lower() in cmd.lower() and proc.pid != os.getpid():
				return True
		except Exception:
			pass
	return False


def bridge_background_notice():
	gw = is_script_running("gateway_local.py")
	wk = is_script_running("brain_worker.py")
	if gw and wk:
		return "Bridge ativo em segundo plano: gateway e worker rodando."
	if gw or wk:
		return "Bridge parcialmente ativo em segundo plano."
	return "Bridge parado em segundo plano."


def latest_version():
	try:
		return LATEST_VERSION_FILE.read_text(encoding="utf-8").strip() or APP_VERSION
	except Exception:
		return APP_VERSION


def update_notice():
	latest = latest_version()
	if latest != APP_VERSION:
		return "Nova versao disponivel: v" + latest + ". Clique em Atualizar app."
	return "App atualizado."

class ControlCenterApp:
	def __init__(self):
		LOG_DIR.mkdir(exist_ok=True)
		self.root = tk.Tk()
		self.root.title(APP_TITLE)
		self.root.configure(bg=DARK_BG)
		self.style = ttk.Style(self.root)
		self.style.theme_use("clam")
		self.style.configure(".", background=DARK_BG, foreground=DARK_TEXT, fieldbackground=DARK_PANEL)
		self.style.configure("TFrame", background=DARK_BG)
		self.style.configure("TLabel", background=DARK_BG, foreground=DARK_TEXT)
		self.style.configure("TButton", background=DARK_PANEL_2, foreground=DARK_TEXT, padding=6)
		self.style.configure("TNotebook", background=DARK_BG, borderwidth=0)
		self.style.configure("TNotebook.Tab", background=DARK_PANEL_2, foreground=DARK_TEXT, padding=(12, 6))
		self.style.map("TNotebook.Tab", background=[("selected", DARK_ACCENT)], foreground=[("selected", DARK_BG)])
		self.root.geometry("980x620")
		self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
		self.status_var = tk.StringVar(value="Inicializando...")
		self.summary_var = tk.StringVar(value="")
		self.process_var = tk.StringVar(value="")
		self.tray_icon = None
		self.last_data = {}
		self.build_ui()
		self.root.after(500, self.start_tray)
		self.refresh()
		self.root.after(3000, self.auto_refresh)
		self.root.after(3000, self.auto_refresh_logs)

	def build_ui(self):
		top = tk.Frame(self.root, bg=DARK_BG)
		top.pack(fill="x", padx=10, pady=6)
		tk.Label(top, text=APP_TITLE, bg=DARK_BG, fg=DARK_TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
		tk.Button(top, text="Atualizar app", command=self.update_app, bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=4).pack(side="right", padx=4)
		tk.Button(top, text="Atualizar", command=self.refresh, bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=4).pack(side="right", padx=4)
		tk.Button(top, text="Abrir pasta", command=self.open_folder, bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=4).pack(side="right", padx=4)
		tk.Label(self.root, textvariable=self.status_var, anchor="w", bg=DARK_PANEL, fg=DARK_TEXT, font=("Segoe UI", 10, "bold"), padx=10, pady=6).pack(fill="x", padx=10, pady=(2,0))
		tk.Label(self.root, textvariable=self.summary_var, anchor="w", bg=DARK_PANEL, fg=DARK_ACCENT, font=("Consolas", 10), padx=10, pady=6).pack(fill="x", padx=10)
		tk.Label(self.root, textvariable=self.process_var, anchor="w", bg=DARK_PANEL, fg=DARK_TEXT, font=("Segoe UI", 10), padx=10, pady=6).pack(fill="x", padx=10, pady=(0,8))
		self.version_var = tk.StringVar(value=update_notice() + " | " + bridge_background_notice())
		tk.Label(self.root, textvariable=self.version_var, anchor="w", bg=DARK_PANEL, fg="#fbbf24", font=("Segoe UI", 10, "bold"), padx=10, pady=6).pack(fill="x", padx=10, pady=(0,8))
		self.tabs = ttk.Notebook(self.root)
		self.tabs.pack(fill="both", expand=True, padx=10, pady=6)
		self.dashboard_text = self.add_tab("Painel")
		self.status_text = self.add_tab("Status JSON")
		self.chats_text = self.add_tab("Chats e comandos")
		self.gateway_text = self.add_tab("Log gateway")
		self.worker_text = self.add_tab("Log workers")
		bottom = tk.Frame(self.root, bg=DARK_BG)
		bottom.pack(fill="x", padx=10, pady=8)
		tk.Button(bottom, text="Ligar AI Bridge", bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=6, command=self.start_bridge).pack(side="left", padx=4)
		tk.Button(bottom, text="Reiniciar AI Bridge", bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=6, command=self.restart_bridge).pack(side="left", padx=4)
		tk.Button(bottom, text="Desligar AI Bridge", bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=6, command=self.stop_processes).pack(side="left", padx=4)
		tk.Button(bottom, text="Limpar logs", bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=6, command=self.clear_logs).pack(side="left", padx=4)
		tk.Button(bottom, text="Minimizar", bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=6, command=self.hide_window).pack(side="left", padx=4)
		tk.Button(bottom, text="Sair", bg=DARK_PANEL_2, fg=DARK_TEXT, activebackground=DARK_ACCENT, activeforeground="#000000", relief="flat", padx=10, pady=6, command=self.exit_app).pack(side="right", padx=4)

	def add_tab(self, title):
		frame = ttk.Frame(self.tabs)
		text = tk.Text(frame, wrap="none", height=12, bg=DARK_PANEL, fg=DARK_TEXT, insertbackground=DARK_TEXT, selectbackground=DARK_ACCENT, selectforeground="#000000", relief="flat", borderwidth=0, highlightthickness=1, highlightbackground=DARK_PANEL_2, highlightcolor=DARK_ACCENT)
		text.pack(fill="both", expand=True)
		self.tabs.add(frame, text=title)
		return text

	def make_icon_image(self):
		img = Image.new("RGB", (64, 64), "white")
		draw = ImageDraw.Draw(img)
		draw.rectangle((8, 8, 56, 56), outline="black", width=3)
		draw.text((20, 22), "AI", fill="black")
		return img

	def start_tray(self):
		if not TRAY_AVAILABLE or self.tray_icon is not None:
			return
		menu = pystray.Menu(pystray.MenuItem("Abrir", self.tray_show), pystray.MenuItem("Sair", self.tray_exit))
		self.tray_icon = pystray.Icon("AI Bridge Local v14", self.make_icon_image(), APP_TITLE, menu)
		self.tray_icon.run_detached()

	def tray_show(self, icon=None, item=None):
		self.root.after(0, self.show_window)
	def tray_exit(self, icon=None, item=None):
		self.root.after(0, self.exit_app)

	def fetch_status(self):
		with urlopen(URL, timeout=5) as response:
			return json.loads(response.read().decode("utf-8"))

	def list_processes(self):
		items = []
		if psutil is None:
			return items
		for proc in psutil.process_iter(["pid", "name", "cmdline"]):
			try:
				cmd = " ".join(proc.info.get("cmdline") or [])
				low = cmd.lower()
				if any(key in low for key in PROCESS_KEYS):
					items.append((proc.info.get("pid"), cmd))
			except Exception:
				pass
		return items

	def update_process_status(self):
		items = self.list_processes()
		gw = sum(1 for pid, cmd in items if "gateway_local.py" in cmd.lower())
		wk = sum(1 for pid, cmd in items if "brain_worker.py" in cmd.lower())
		self.process_var.set("Processos ocultos/ativos: gateway={0} workers={1} repo={2}".format(gw, wk, ROOT))

	def count_processes(self):
		items = self.list_processes()
		gateways = sum(1 for pid, cmd in items if 'gateway_local.py' in cmd.lower())
		workers = sum(1 for pid, cmd in items if 'brain_worker.py' in cmd.lower())
		return workers, gateways

	def render_dashboard(self, data):
		counts = data.get("command_status", {})
		workers, gateways = self.count_processes()
		recent = data.get("recent_commands", []) or []
		rows = []
		rows.append("AI Bridge Local - Painel operacional")
		rows.append("=" * 46)
		rows.append("")
		rows.append(("[OK] Gateway online" if gateways else "[ALERTA] Gateway offline"))
		rows.append("Workers ativos: " + str(workers))
		rows.append("Comandos recentes: " + str(len(recent)))
		rows.append("")
		rows.append("Status da fila/comandos")
		rows.append(" acked: " + str(counts.get("acked", 0)))
		rows.append(" queued: " + str(counts.get("queued", 0)))
		rows.append(" delivering: " + str(counts.get("delivering", 0)))
		rows.append(" failed: " + str(counts.get("failed", 0)))
		rows.append("")
		rows.append("Aviso do sistema:")
		rows.append(" " + bridge_background_notice())
		rows.append(" " + update_notice())
		rows.append("")
		rows.append("Operacao recomendada")
		rows.append(" Ligar AI Bridge: inicia gateway + workers internos.")
		rows.append(" Reiniciar AI Bridge: limpa processos e sobe tudo novamente.")
		rows.append(" Logs: atualizacao automatica a cada 1 segundo.")
		rows.append("")
		rows.append("Caminhos")
		rows.append(" Repo: " + str(ROOT))
		rows.append(" Worker log: " + str(WORKER_LOG))
		return chr(10).join(rows)

	def render_chats(self, data):
		rows = []
		recent = data.get("recent_commands", []) or []
		rows.append("Comandos recentes: " + str(len(recent)))
		rows.append("")
		seen = {}
		for item in recent:
			src = item.get("source_chat_id", "")
			dst = item.get("target_chat_id", "")
			st = item.get("status", "")
			act = item.get("action", "")
			cid = item.get("command_id", "")
			rows.append(st + " | " + act + " | " + cid)
			rows.append(" " + src + " -> " + dst)
			rows.append("")
			seen[src] = seen.get(src, 0) + 1
			seen[dst] = seen.get(dst, 0) + 1
		rows.append("Chats vistos nos comandos recentes:")
		for chat, count in sorted(seen.items(), key=lambda x: (-x[1], x[0])):
			if chat:
				rows.append(str(count) + " " + chat)
		return chr(10).join(rows)

	def read_tail(self, path, limit=12000):
		try:
			if not path.exists():
				return "Log ainda vazio: " + str(path)
			data = path.read_text(encoding="utf-8", errors="replace")
			return data[-limit:]
		except Exception as exc:
			return "Erro lendo log: " + str(exc)

	def set_text(self, widget, value):
		widget.delete("1.0", "end")
		widget.insert("end", value)
		widget.see("end")

	def write_worker_monitor_log(self):
		now = time.strftime("%Y-%m-%d %H:%M:%S")
		try:
			LOG_DIR.mkdir(exist_ok=True)
			line = "[central-monitor] " + now + " repo=" + str(ROOT) + chr(10)
			with open(MONITOR_LOG, "a", encoding="utf-8", errors="replace") as f:
				f.write(line)
				f.flush()
		except Exception as exc:
			try:
				with open(MONITOR_LOG, "a", encoding="utf-8", errors="replace") as f:
					f.write("[central-monitor-error] " + now + " " + str(exc) + chr(10))
			except Exception:
				pass

	def refresh(self):
		self.update_process_status()
		try:
			self.version_var.set(update_notice() + " | " + bridge_background_notice())
		except Exception:
			pass
		self.write_worker_monitor_log()
		try:
			data = self.fetch_status()
			self.last_data = data
			counts = data.get("command_status", {})
			self.status_var.set("Gateway online - " + data.get("timestamp", ""))
			self.summary_var.set("acked={0} queued={1} delivering={2} failed={3}".format(counts.get("acked", 0), counts.get("queued", 0), counts.get("delivering", 0), counts.get("failed", 0)))
			self.set_text(self.dashboard_text, self.render_dashboard(data))
			self.set_text(self.status_text, json.dumps(data, indent=2, ensure_ascii=False))
			self.set_text(self.chats_text, self.render_chats(data))
		except Exception as exc:
			self.status_var.set("Gateway indisponivel - clique em Ligar AI Bridge")
			self.summary_var.set(str(exc))
			self.set_text(self.dashboard_text, "Gateway indisponivel - clique em Ligar AI Bridge" + chr(10) + str(exc))
		self.set_text(self.gateway_text, self.read_tail(GATEWAY_LOG))
		self.set_text(self.worker_text, self.read_tail(WORKER_LOG))

	def auto_refresh(self):
		try:
			self.refresh()
		finally:
			self.root.after(3000, self.auto_refresh)

	def auto_refresh_logs(self):
		try:
			self.set_text(self.gateway_text, self.read_tail(GATEWAY_LOG))
			self.set_text(self.worker_text, self.read_tail(WORKER_LOG))
		finally:
			self.root.after(3000, self.auto_refresh_logs)

	def python_exe(self):
		return shutil.which("python") or sys.executable

	def start_python_hidden(self, script_name, log_path):
		script = ROOT / script_name
		if not script.exists():
			messagebox.showerror(APP_TITLE, "Arquivo nao encontrado: " + str(script))
			return
		LOG_DIR.mkdir(exist_ok=True)
		log = open(log_path, "a", encoding="utf-8", errors="replace")
		log.write("\n--- START " + script_name + " " + time.strftime("%Y-%m-%d %H:%M:%S") + " ---\n")
		log.flush()
		env = os.environ.copy()
		env["PYTHONUNBUFFERED"] = "1"
		subprocess.Popen([self.python_exe(), "-u", str(script)], cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT, creationflags=CREATE_NO_WINDOW, env=env)
		time.sleep(1)
		self.refresh()

	def start_bridge(self):
		self.start_gateway()
		time.sleep(1)
		self.start_pool()

	def restart_bridge(self):
		self.stop_processes()
		time.sleep(1)
		self.start_bridge()

	def start_gateway(self):
		if is_script_running("gateway_local.py"):
			self.log("Gateway ja esta ativo; nao vou abrir outra instancia.")
			return
		self.start_python_hidden("gateway_local.py", GATEWAY_LOG)
	def start_worker(self):
		self.start_python_hidden("brain_worker.py", WORKER_LOG)
	def start_pool(self):
		if is_script_running("brain_worker.py"):
			self.log("Worker ja esta ativo; nao vou abrir outra instancia.")
			return
		for i in range(4):
			self.start_python_hidden("brain_worker.py", WORKER_LOG)
		time.sleep(1)
		self.refresh()

	def clear_logs(self):
		for path in [GATEWAY_LOG, WORKER_LOG]:
			path.write_text("", encoding="utf-8")
		self.refresh()

	def stop_processes(self):
		if psutil is None:
			messagebox.showerror(APP_TITLE, "psutil nao disponivel")
			return
		stopped = 0
		for pid, cmd in self.list_processes():
			try:
				psutil.Process(pid).terminate()
				stopped += 1
			except Exception:
				pass
		time.sleep(1)
		self.refresh()
		messagebox.showinfo(APP_TITLE, "Processos sinalizados para parar: " + str(stopped))

	def update_app(self):
		updater = ROOT / "packaging" / "update_control_center.py"
		if not updater.exists():
			messagebox.showerror(APP_TITLE, "Atualizador nao encontrado: " + str(updater))
			return
		UPDATE_LOG.write_text("Atualizacao iniciada pela Central. A janela sera fechada e reaberta.\n", encoding="utf-8")
		subprocess.Popen([self.python_exe(), str(updater)], cwd=str(ROOT), creationflags=CREATE_NO_WINDOW)
		self.exit_app()

	def open_folder(self):
		subprocess.Popen(["explorer", str(ROOT)])
	def hide_window(self):
		self.root.withdraw()
	def show_window(self):
		self.root.deiconify()
		self.root.lift()
		self.refresh()
	def exit_app(self):
		if self.tray_icon is not None:
			self.tray_icon.stop()
		self.root.destroy()
	def run(self):
		self.root.mainloop()

ControlCenterApp().run()
