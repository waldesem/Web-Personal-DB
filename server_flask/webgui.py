"""
Original code here https://github.com/ClimenteA/flaskwebgui
"""

import os
import platform
import shutil
import signal
import socketserver
import subprocess
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from multiprocessing import Process
from threading import Thread
from typing import Any, Callable, Dict, List, Union

import psutil
from wsgi import wsgi_server

FLASKWEBGUI_USED_PORT = None
FLASKWEBGUI_BROWSER_PROCESS = None

OPERATING_SYSTEM = platform.system().lower()
PY = "python3" if OPERATING_SYSTEM == "linux" else "python"


def get_free_port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        return s.server_address[1]


def kill_port(port: int):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                psutil.Process(conn.pid).send_signal(signal.SIGTERM)
            except psutil.AccessDenied:
                continue
            break


def close_application():
    if FLASKWEBGUI_BROWSER_PROCESS is not None:
        FLASKWEBGUI_BROWSER_PROCESS.terminate()

    kill_port(FLASKWEBGUI_USED_PORT)


def find_browser_on_linux():
    paths = ["/snap/bin/chromium", "/snap/bin/firefox"]
    for path in paths:
        if os.path.exists(path):
            return path

    for path in paths:
        try:
            bp = subprocess.check_output(["which", os.path.basename(path)], text=True).strip()
            if os.path.exists(bp):
                return bp
        except subprocess.CalledProcessError:
            pass

    return None


def find_browser_on_windows():
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None


browser_path_dispacher: Dict[str, Callable[[], str]] = {
    "windows": find_browser_on_windows,
    "linux": find_browser_on_linux,
}


class ServerFlask:
    @staticmethod
    def get_server_kwargs(**kwargs):
        return {"app": kwargs.get("app"), "port": kwargs.get("port")}

    @staticmethod
    def server(**server_kwargs):
        app = server_kwargs.pop("app", None)
        server_kwargs.pop("debug", None)
        wsgi_server(app, **server_kwargs)


@dataclass
class FlaskUI:
    server: Callable[[Any], None] = None
    server_kwargs: dict = None
    app: Any = None
    port: int = None
    on_startup: Callable = None
    on_shutdown: Callable = None
    browser_path: str = None
    browser_command: List[str] = None
    browser_pid: int = None

    def __post_init__(self):
        self.__keyboard_interrupt = False
        global FLASKWEBGUI_USED_PORT

        self.port = self.port or (
            self.server_kwargs.get("port") if self.server_kwargs else get_free_port()
        )
        FLASKWEBGUI_USED_PORT = self.port

        self.server = self.server or ServerFlask().server

        self.profile_dir = tempfile.mkdtemp(prefix=f"flaskwebgui{uuid.uuid4().hex}")
        self.url = f"http://127.0.0.1:{self.port}"

        self.browser_path = (
            self.browser_path
            or browser_path_dispacher.get(OPERATING_SYSTEM, lambda: None)()
        )
        self.browser_command = self.browser_command or (
            [PY, "-m", "webbrowser", "-n", self.url]
            if not self.browser_path
            else self.get_browser_command()
        )

    def get_browser_command(self):
        flags = [
            self.browser_path,
            f"--app={self.url}",
            f"--user-data-dir={self.profile_dir}",
            "--new-window",
            "--start-maximized",
            "--no-default-browser-check",
            "--allow-insecure-localhost",
            "--no-first-run",
            "--disable-sync",
        ]

        return flags

    def start_browser(self, server_process: Union[Thread, Process]):
        # print("Command:", " ".join(self.browser_command))
        global FLASKWEBGUI_BROWSER_PROCESS

        FLASKWEBGUI_BROWSER_PROCESS = subprocess.Popen(self.browser_command)
        self.browser_pid = FLASKWEBGUI_BROWSER_PROCESS.pid
        FLASKWEBGUI_BROWSER_PROCESS.wait()

        if self.browser_path is None:
            while self.__keyboard_interrupt is False:
                time.sleep(1)

        if isinstance(server_process, Process):
            if self.on_shutdown is not None:
                self.on_shutdown()
            self.browser_pid = None
            shutil.rmtree(self.profile_dir, ignore_errors=True)
            server_process.kill()
        else:
            if self.on_shutdown is not None:
                self.on_shutdown()
            self.browser_pid = None
            shutil.rmtree(self.profile_dir, ignore_errors=True)
            kill_port(self.port)

    def run(self):
        if self.on_startup:
            self.on_startup()

        with ThreadPoolExecutor(max_workers=2) as executor:
            server_future = executor.submit(self.server, **(self.server_kwargs or {}))
            browser_future = executor.submit(self.start_browser, server_future)

            try:
                server_future.result()
                browser_future.result()
            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")

        return server_future, browser_future
