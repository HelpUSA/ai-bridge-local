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

# AI_BRIDGE_MANAGED:CONTROL_CENTER_SINGLE_INSTANCE_0585:START
def _ai_bridge_control_center_single_instance_0585():
    """Keep exactly one Control Center process on Windows."""
    import ctypes as _ab_si_ctypes
    import sys as _ab_si_sys
    from ctypes import wintypes as _ab_si_wintypes

    if _ab_si_sys.platform != "win32":
        return None

    error_already_exists = 183

    kernel32 = _ab_si_ctypes.WinDLL(
        "kernel32",
        use_last_error=True,
    )

    create_mutex = kernel32.CreateMutexW
    create_mutex.argtypes = [
        _ab_si_wintypes.LPVOID,
        _ab_si_wintypes.BOOL,
        _ab_si_wintypes.LPCWSTR,
    ]
    create_mutex.restype = _ab_si_wintypes.HANDLE

    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [
        _ab_si_wintypes.HANDLE,
    ]
    close_handle.restype = _ab_si_wintypes.BOOL

    _ab_si_ctypes.set_last_error(0)

    mutex_handle = create_mutex(
        None,
        False,
        (
            "Local\\"
            "AI_Bridge_Local_"
            "Control_Center_0585"
        ),
    )

    last_error = (
        _ab_si_ctypes.get_last_error()
    )

    if not mutex_handle:
        raise OSError(
            last_error,
            "CreateMutexW failed",
        )

    if last_error == error_already_exists:
        close_handle(
            mutex_handle
        )

        try:
            user32 = (
                _ab_si_ctypes.WinDLL(
                    "user32",
                    use_last_error=True,
                )
            )

            message_box = user32.MessageBoxW
            message_box.argtypes = [
                _ab_si_wintypes.HWND,
                _ab_si_wintypes.LPCWSTR,
                _ab_si_wintypes.LPCWSTR,
                _ab_si_wintypes.UINT,
            ]
            message_box.restype = (
                _ab_si_ctypes.c_int
            )

            message_box(
                None,
                (
                    "A Central de Controle "
                    "j? est? aberta."
                ),
                (
                    "AI Bridge Local 0.5.86"
                ),
                0x00000040,
            )

        except Exception:
            pass

        raise SystemExit(0)

    return mutex_handle


if __name__ == "__main__":
    _AI_BRIDGE_CONTROL_CENTER_MUTEX_0585 = (
        _ai_bridge_control_center_single_instance_0585()
    )
# AI_BRIDGE_MANAGED:CONTROL_CENTER_SINGLE_INSTANCE_0585:END

# AI_BRIDGE_MANAGED:CONTROL_CENTER_AUTOSTART_0585:START
def _ai_bridge_control_center_autostart_0585():
    # Start gateway and worker in the background when the app opens.
    import datetime as _ab_datetime
    import json as _ab_json
    import os as _ab_os
    import re as _ab_re
    import subprocess as _ab_subprocess
    import sys as _ab_sys
    import threading as _ab_threading
    import time as _ab_time
    import urllib.request as _ab_urlrequest
    from pathlib import Path as _AbPath

    def _ab_runner():
        version = "0.5.86"

        root = (
            _AbPath(__file__)
            .resolve()
            .parents[1]
        )

        logs = root / "logs"
        temp = root / "temp"

        logs.mkdir(
            parents=True,
            exist_ok=True,
        )

        temp.mkdir(
            parents=True,
            exist_ok=True,
        )

        log_path = (
            logs
            / "control_center_autostart.log"
        )

        lock_path = (
            temp
            / "control_center_autostart.lock"
        )

        lock_fd = None

        def log(message):
            try:
                stamp = (
                    _ab_datetime
                    .datetime
                    .now()
                    .astimezone()
                    .isoformat()
                )

                with log_path.open(
                    "a",
                    encoding="utf-8",
                ) as handle:
                    handle.write(
                        f"{stamp} {message}\n"
                    )

            except Exception:
                pass

        def endpoint_ok(
            uri,
            expected_service,
        ):
            try:
                request = (
                    _ab_urlrequest.Request(
                        uri,
                        headers={
                            "Accept":
                            "application/json",
                        },
                        method="GET",
                    )
                )

                with _ab_urlrequest.urlopen(
                    request,
                    timeout=1.5,
                ) as response:
                    payload = _ab_json.loads(
                        response
                        .read()
                        .decode(
                            "utf-8",
                            errors="replace",
                        )
                    )

                return (
                    payload.get("service")
                    == expected_service
                    and payload.get("version")
                    == version
                )

            except Exception:
                return False

        def process_count(script_name):
            if _ab_os.name != "nt":
                return 0

            pattern = (
                _ab_re
                .escape(script_name)
                .replace(
                    "'",
                    "''",
                )
            )

            command = (
                "$ErrorActionPreference="
                "'SilentlyContinue';"

                "$items=@("
                "Get-CimInstance "
                "Win32_Process | "

                "Where-Object { "
                "$_.CommandLine "
                "-and "

                "$_.CommandLine "
                "-match '"
                + pattern
                + "' "
                "-and "

                "$_.CommandLine "
                "-notmatch "
                "'(^|\\s)--help($|\\s)'"
                " });"

                "Write-Output "
                "$items.Count"
            )

            try:
                result = (
                    _ab_subprocess.run(
                        [
                            "powershell.exe",
                            "-NoProfile",
                            "-NonInteractive",
                            "-ExecutionPolicy",
                            "Bypass",
                            "-Command",
                            command,
                        ],
                        cwd=str(root),
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        stdout=(
                            _ab_subprocess
                            .PIPE
                        ),
                        stderr=(
                            _ab_subprocess
                            .DEVNULL
                        ),
                        timeout=8,
                        creationflags=getattr(
                            _ab_subprocess,
                            "CREATE_NO_WINDOW",
                            0,
                        ),
                    )
                )

                values = (
                    _ab_re.findall(
                        r"\d+",
                        result.stdout or "",
                    )
                )

                if not values:
                    return 0

                return int(values[-1])

            except Exception as error:
                log(
                    "process_count_error "
                    f"script={script_name} "
                    "error="
                    f"{type(error).__name__}: "
                    f"{error}"
                )

                return 0

        def console_python():
            executable = (
                _AbPath(
                    _ab_sys.executable
                )
                .resolve()
            )

            if (
                executable.name.lower()
                == "pythonw.exe"
            ):
                candidate = (
                    executable.with_name(
                        "python.exe"
                    )
                )

                if candidate.is_file():
                    return candidate

            return executable

        def spawn(
            script_name,
            log_name,
        ):
            script_path = (
                root
                / script_name
            )

            if not script_path.is_file():
                log(
                    f"missing_script="
                    f"{script_path}"
                )

                return None

            python_executable = (
                console_python()
            )

            stdout_path = (
                logs
                / f"{log_name}.stdout.log"
            )

            stderr_path = (
                logs
                / f"{log_name}.stderr.log"
            )

            flags = 0

            if _ab_os.name == "nt":
                flags = getattr(
                    _ab_subprocess,
                    "CREATE_NO_WINDOW",
                    0,
                )

            environment = (
                _ab_os.environ.copy()
            )

            environment.setdefault(
                "PYTHONUTF8",
                "1",
            )

            environment.setdefault(
                "AI_BRIDGE_COMMAND_HOST",
                "127.0.0.1",
            )

            environment.setdefault(
                "AI_BRIDGE_COMMAND_PORT",
                "8767",
            )

            environment.pop(
                "AI_BRIDGE_ENABLE_LOCAL_RUN",
                None,
            )

            with stdout_path.open(
                "ab",
                buffering=0,
            ) as stdout_handle:

                with stderr_path.open(
                    "ab",
                    buffering=0,
                ) as stderr_handle:

                    process = (
                        _ab_subprocess.Popen(
                            [
                                str(
                                    python_executable
                                ),
                                "-X",
                                "utf8",
                                "-u",
                                str(
                                    script_path
                                ),
                            ],
                            cwd=str(root),
                            env=environment,
                            stdin=(
                                _ab_subprocess
                                .DEVNULL
                            ),
                            stdout=(
                                stdout_handle
                            ),
                            stderr=(
                                stderr_handle
                            ),
                            creationflags=flags,
                            close_fds=True,
                        )
                    )

            log(
                f"started={script_name} "
                f"pid={process.pid} "
                f"python="
                f"{python_executable}"
            )

            return process.pid

        try:
            try:
                lock_fd = _ab_os.open(
                    str(lock_path),
                    (
                        _ab_os.O_CREAT
                        | _ab_os.O_EXCL
                        | _ab_os.O_WRONLY
                    ),
                )

            except FileExistsError:
                try:
                    age = (
                        _ab_time.time()
                        - lock_path
                        .stat()
                        .st_mtime
                    )

                except Exception:
                    age = 0

                if age < 60:
                    log(
                        "bootstrap_already_"
                        "running "
                        f"age={age:.1f}"
                    )

                    return

                try:
                    lock_path.unlink()

                except Exception:
                    log(
                        "stale_bootstrap_"
                        "lock_could_not_"
                        "be_removed"
                    )

                    return

                lock_fd = _ab_os.open(
                    str(lock_path),
                    (
                        _ab_os.O_CREAT
                        | _ab_os.O_EXCL
                        | _ab_os.O_WRONLY
                    ),
                )

            _ab_os.write(
                lock_fd,
                str(
                    _ab_os.getpid()
                ).encode(
                    "ascii",
                    errors="ignore",
                ),
            )

            gateway_ok = endpoint_ok(
                (
                    "http://127.0.0.1:"
                    "8766/health"
                ),
                "ai-bridge-local",
            )

            command_plane_ok = endpoint_ok(
                (
                    "http://127.0.0.1:"
                    "8767/health"
                ),
                "ai-bridge-command-plane",
            )

            gateway_processes = (
                process_count(
                    "gateway_local.py"
                )
            )

            worker_processes = (
                process_count(
                    "brain_worker.py"
                )
            )

            log(
                "preflight "
                f"gateway="
                f"{int(gateway_ok)} "
                f"command_plane="
                f"{int(command_plane_ok)} "
                f"gateway_processes="
                f"{gateway_processes} "
                f"worker_processes="
                f"{worker_processes}"
            )

            if (
                not gateway_ok
                or not command_plane_ok
            ):
                if gateway_processes == 0:
                    spawn(
                        "gateway_local.py",
                        "gateway_autostart",
                    )

                else:
                    log(
                        "gateway_process_"
                        "present_but_"
                        "endpoint_unhealthy "
                        f"gateway="
                        f"{int(gateway_ok)} "
                        f"command_plane="
                        f"{int(command_plane_ok)}"
                    )

            if worker_processes == 0:
                spawn(
                    "brain_worker.py",
                    "worker_autostart",
                )

            for _ in range(20):
                current_gateway = endpoint_ok(
                    (
                        "http://127.0.0.1:"
                        "8766/health"
                    ),
                    "ai-bridge-local",
                )

                current_command_plane = (
                    endpoint_ok(
                        (
                            "http://127.0.0.1:"
                            "8767/health"
                        ),
                        (
                            "ai-bridge-"
                            "command-plane"
                        ),
                    )
                )

                current_workers = (
                    process_count(
                        "brain_worker.py"
                    )
                )

                if (
                    current_gateway
                    and current_command_plane
                    and current_workers > 0
                ):
                    log(
                        "postflight "
                        "gateway=1 "
                        "command_plane=1 "
                        "worker=1"
                    )

                    break

                _ab_time.sleep(0.5)

            else:
                log(
                    "postflight_incomplete "
                    f"gateway="
                    f"{int(current_gateway)} "
                    f"command_plane="
                    f"{int(current_command_plane)} "
                    f"worker_processes="
                    f"{current_workers}"
                )

        except Exception as error:
            log(
                "bootstrap_error="
                f"{type(error).__name__}: "
                f"{error}"
            )

        finally:
            if lock_fd is not None:
                try:
                    _ab_os.close(lock_fd)

                except Exception:
                    pass

            try:
                lock_path.unlink()

            except Exception:
                pass

    _ab_threading.Thread(
        target=_ab_runner,
        name=(
            "ai-bridge-control-"
            "center-autostart"
        ),
        daemon=True,
    ).start()


if __name__ == "__main__":
    _ai_bridge_control_center_autostart_0585()
# AI_BRIDGE_MANAGED:CONTROL_CENTER_AUTOSTART_0585:END

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
APP_TITLE = "AI Bridge Local - Central de Controle 0.5.86"
if getattr(sys, "frozen", False):
	ROOT = Path(sys.executable).resolve().parents[2]
else:
	ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:8766/control/status"
DIAGNOSTICS_URL = "http://127.0.0.1:8766/control/diagnostics"
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

# AI_BRIDGE_MANAGED:CONTROL_CENTER_ASYNC_IMPORTS_0585:START
import queue as _cc_queue
import threading as _cc_threading
import sqlite3 as _cc_sqlite3
# AI_BRIDGE_MANAGED:CONTROL_CENTER_ASYNC_IMPORTS_0585:END

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
		# AI_BRIDGE_MANAGED:CONTROL_CENTER_ASYNC_INIT_0585:START
		self.tray_icon = None
		self.last_data = {}
		self._refresh_results = _cc_queue.Queue()
		self._refresh_inflight = False
		self._refresh_pending = False
		self.build_ui()
		self.root.after(100, self._drain_refresh_results)
		self.root.after(500, self.start_tray)
		self.refresh()
		self.root.after(3000, self.auto_refresh)
		# AI_BRIDGE_MANAGED:CONTROL_CENTER_ASYNC_INIT_0585:END

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
		errors = []
		for endpoint in [DIAGNOSTICS_URL, URL]:
			try:
				with urlopen(endpoint, timeout=5) as response:
					data = json.loads(response.read().decode("utf-8"))
					data["_control_center_endpoint"] = endpoint
					if endpoint == URL:
						data["_control_center_fallback"] = "control/status"
					return data
			except Exception as exc:
				errors.append(endpoint + " -> " + str(exc))
		raise RuntimeError("Gateway status unavailable: " + " | ".join(errors))

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

	# AI_BRIDGE_MANAGED:CONTROL_CENTER_DISPLAY_COUNTS_0585:START
	def _build_display_counts(self, data):
		cached = data.get("_control_center_display_counts")
		if isinstance(cached, dict):
			return cached

		command_status = data.get("command_status", {}) or {}
		queue_counts = data.get("queue", {}) or {}
		counts = {}
		for key in ("acked", "queued", "delivering", "failed"):
			candidates = []
			for source in (command_status, queue_counts):
				try:
					candidates.append(int(source.get(key, 0) or 0))
				except Exception:
					pass
			counts[key] = max(candidates or [0])

		database = ROOT / "queue_local.db"
		try:
			uri = database.resolve().as_uri() + "?mode=ro"
			with _cc_sqlite3.connect(
				uri,
				uri=True,
				timeout=1.5,
			) as connection:
				connection.execute("PRAGMA query_only=ON")
				connection.execute("PRAGMA busy_timeout=1500")
				row = connection.execute(
					"SELECT COUNT(*) "
					"FROM commands "
					"WHERE lower(status)=?",
					("acked",),
				).fetchone()
				database_acked = int(row[0] if row else 0)
				counts["acked"] = max(
					counts.get("acked", 0),
					database_acked,
				)
		except Exception:
			pass

		data["_control_center_display_counts"] = counts
		return counts
	# AI_BRIDGE_MANAGED:CONTROL_CENTER_DISPLAY_COUNTS_0585:END

	def render_dashboard(self, data):
		counts = data.get("_control_center_display_counts") or data.get("command_status", {}) or data.get("queue", {})
		# AI_BRIDGE_MANAGED:CONTROL_CENTER_PROCESS_COUNTS_0585:START
		workers = data.get("_control_center_workers")
		gateways = data.get("_control_center_gateways")
		if workers is None or gateways is None:
		        workers, gateways = self.count_processes()
		# AI_BRIDGE_MANAGED:CONTROL_CENTER_PROCESS_COUNTS_0585:END
		recent = data.get("recent_commands", []) or []
		rows = []
		rows.append("AI Bridge Local - Painel operacional")
		rows.append("=" * 46)
		rows.append("")
		rows.append(("[OK] Gateway online" if gateways else "[ALERTA] Gateway offline"))
		rows.append("Worker ativo: " + str(workers))
		rows.append("Comandos recentes: " + str(len(recent)))
		rows.append("Endpoint: " + str(data.get("_control_center_endpoint", URL)))
		if data.get("_control_center_fallback"):
			rows.append("Fallback: " + str(data.get("_control_center_fallback")))
		if data.get("gateway_first"):
			rows.append("Modo gateway-first: ativo")
			policy = data.get("route_policy", {}) if isinstance(data.get("route_policy", {}), dict) else {}
			if policy:
				rows.append("Politica de rota: " + str(policy.get("mode", "")))
				rows.append(" Direct interchat: " + ("ativo" if policy.get("direct_interchat_enabled") else "bloqueado"))
				if policy.get("direct_interchat_disabled_reason"):
					rows.append(" Motivo: " + str(policy.get("direct_interchat_disabled_reason")))
				rows.append(" Inter-agent route: " + str(policy.get("inter_agent_message_route", "")))
				rows.append(" Local capability route: " + str(policy.get("local_capability_route", "")))
				if policy.get("blocked_route") and policy.get("replacement_route"):
					rows.append(" Route lock: " + str(policy.get("blocked_route")) + " -> " + str(policy.get("replacement_route")))
		# AI_BRIDGE_MANAGED:CONTROL_CENTER_QUEUE_HEALTH_0585:START
		rows.append("")
		queued_count = int(counts.get("queued", 0) or 0)
		delivering_count = int(counts.get("delivering", 0) or 0)
		active_count = queued_count + delivering_count
		rows.append("Saude operacional atual")
		rows.append(" [OK] Fila ativa vazia" if active_count == 0 else " [ATENCAO] Fila ativa com trabalho pendente")
		rows.append(" queued: " + str(queued_count))
		rows.append(" delivering: " + str(delivering_count))
		rows.append("")
		rows.append("Historico acumulado")
		rows.append(" acked: " + str(counts.get("acked", 0)))
		rows.append(" failed: " + str(counts.get("failed", 0)))
		# AI_BRIDGE_MANAGED:CONTROL_CENTER_QUEUE_HEALTH_0585:END
		queue = data.get("queue", {}) or {}
		active_targets = queue.get("active_targets", []) or []
		if active_targets:
			rows.append("")
			rows.append("Targets ativos")
			for item in active_targets[:8]:
				rows.append(" " + item.get("status", "") + " " + str(item.get("count", 0)) + " -> " + item.get("target_chat_id", ""))
		diagnostics = data.get("diagnostics", {}) or {}
		control_plane = data.get("control_plane", {}) or {}
		if diagnostics or control_plane:
			rows.append("")
			# AI_BRIDGE_MANAGED:CONTROL_CENTER_HISTORY_DIAGNOSTICS_0585:START
			rows.append("Historico de falhas e diagnostico")
			rows.append(" dead_letters (historico): " + str(diagnostics.get("dead_letter_count", 0)))
			rows.append(" recent_errors exibidos: " + str(len(diagnostics.get("recent_errors", []) or [])))
			# AI_BRIDGE_MANAGED:CONTROL_CENTER_HISTORY_DIAGNOSTICS_0585:END
			if control_plane:
				rows.append(" extension_role: " + str(control_plane.get("extension_role", "")))
				rows.append(" chats_role: " + str(control_plane.get("chats_role", "")))
			checks = diagnostics.get("recommended_next_checks", []) or []
			if checks:
				rows.append(" next_checks: " + ", ".join(checks[:5]))
		rows.append("")
		rows.append("Aviso do sistema:")
		rows.append(" " + bridge_background_notice())
		rows.append(" " + update_notice())
		rows.append("")
		rows.append("Operacao recomendada")
		rows.append(" Ligar AI Bridge: inicia gateway + worker interno.")
		rows.append(" Reiniciar AI Bridge: limpa processos e sobe tudo novamente.")
		rows.append("Logs e diagnosticos: atualizacao assincrona a cada 3 segundos.")
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

	# AI_BRIDGE_MANAGED:CONTROL_CENTER_ASYNC_REFRESH_0585:START
	def _collect_refresh_payload(self):
		try:
			items = self.list_processes()
			gateways = sum(1 for pid, cmd in items if "gateway_local.py" in cmd.lower())
			workers = sum(1 for pid, cmd in items if "brain_worker.py" in cmd.lower())
			self.write_worker_monitor_log()
			data = self.fetch_status()
			data["_control_center_gateways"] = gateways
			data["_control_center_workers"] = workers
			counts = self._build_display_counts(data)
			queued_count = int(counts.get("queued", 0) or 0)
			delivering_count = int(counts.get("delivering", 0) or 0)
			active_count = queued_count + delivering_count
			return {
				"ok": True,
				"data": data,
				"version_text": update_notice() + " | " + bridge_background_notice(),
				"process_text": "Processos ocultos/ativos: gateway={0} workers={1} repo={2}".format(
					gateways,
					workers,
					ROOT,
				),
				"status_text": "Gateway online - " + data.get("timestamp", ""),
				"summary_text": "fila_ativa={0} queued={1} delivering={2} | historico: acked={3} failed={4}".format(
					active_count,
					queued_count,
					delivering_count,
					counts.get("acked", 0),
					counts.get("failed", 0),
				),
				"dashboard_text": self.render_dashboard(data),
				"status_json": json.dumps(data, indent=2, ensure_ascii=False),
				"chats_text": self.render_chats(data),
				"gateway_text": self.read_tail(GATEWAY_LOG),
				"worker_text": self.read_tail(WORKER_LOG),
			}
		except Exception as exc:
			return {
				"ok": False,
				"error": str(exc),
				"gateway_text": self.read_tail(GATEWAY_LOG),
				"worker_text": self.read_tail(WORKER_LOG),
			}

	def _refresh_worker(self):
		payload = self._collect_refresh_payload()
		self._refresh_results.put(payload)

	def _apply_refresh_payload(self, payload):
		self._refresh_inflight = False
		if payload.get("ok"):
			self.last_data = payload["data"]
			self.version_var.set(payload["version_text"])
			self.process_var.set(payload["process_text"])
			self.status_var.set(payload["status_text"])
			self.summary_var.set(payload["summary_text"])
			self.set_text(self.dashboard_text, payload["dashboard_text"])
			self.set_text(self.status_text, payload["status_json"])
			self.set_text(self.chats_text, payload["chats_text"])
		else:
			error = payload.get("error", "erro desconhecido")
			self.status_var.set("Gateway indisponivel - ""clique em Ligar AI Bridge")
			self.summary_var.set(error)
			self.set_text(self.dashboard_text, "Gateway indisponivel - ""clique em Ligar AI Bridge" + chr(10) + error)
		self.set_text(self.gateway_text, payload.get("gateway_text", ""))
		self.set_text(self.worker_text, payload.get("worker_text", ""))
		if self._refresh_pending:
			self._refresh_pending = False
			self.refresh()

	def _drain_refresh_results(self):
		try:
			while True:
				payload = self._refresh_results.get_nowait()
				self._apply_refresh_payload(payload)
		except _cc_queue.Empty:
			pass
		try:
			self.root.after(100, self._drain_refresh_results)
		except tk.TclError:
			pass

	def refresh(self):
		if self._refresh_inflight:
			self._refresh_pending = True
			return
		self._refresh_inflight = True
		try:
			thread = _cc_threading.Thread(
				target=self._refresh_worker,
				name="ai-bridge-control-center-refresh",
				daemon=True,
			)
			thread.start()
		except Exception as exc:
			self._refresh_inflight = False
			self.status_var.set("Falha iniciando atualizacao: " + str(exc))
	# AI_BRIDGE_MANAGED:CONTROL_CENTER_ASYNC_REFRESH_0585:END

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

	def open_diagnostics_viewer(self):
		try:
			subprocess.Popen([sys.executable, str(ROOT / 'app_windows' / 'diagnostics_viewer.py')], cwd=str(ROOT), creationflags=CREATE_NO_WINDOW)
		except Exception as exc:
			messagebox.showerror('Diagnosticos', str(exc))

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
		for i in range(1):
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
