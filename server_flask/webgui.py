"""WebGUI module."""

import platform
import shutil
import signal
import subprocess
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
from pathlib import Path

import psutil
from flask import Flask

from wsgi import wsgi_server

operating_sys = platform.system().lower()


def find_browser_on_linux() -> str:
    """Find the path to the default browser on Linux."""
    paths = ["/snap/bin/chromium", "/snap/bin/firefox"]
    for path in paths:
        if Path(path).exists():
            return path
    return None


def find_browser_on_windows() -> str:
    """Find the path to the default browser on Windows."""
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    for path in paths:
        if Path(path).exists():
            return path
    return None


def make_browser_command(browser_path: str, url: str, profile_dir: str) -> list[str]:
    """Make the command to start the browser."""
    return (
        [
            browser_path,
            f"--app={url}",
            f"--user-data-dir={profile_dir}",
            "--new-window",
            "--start-maximized",
            "--no-default-browser-check",
            "--allow-insecure-localhost",
            "--no-first-run",
            "--disable-sync",
            "--disable-extensions",
            "--disable-default-apps",
            "--window-size=1280,960",
        ]
        if browser_path
        else [
            "python3" if operating_sys == "linux" else "python",
            "-m",
            "webbrowser",
            "-n",
            url,
        ]
    )


def kill_port(port: int) -> None:
    """Kill the process listening on the specified port."""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                psutil.Process(conn.pid).send_signal(signal.SIGTERM)
            except psutil.AccessDenied:
                continue
            break


def start_browser(server_process: Process, address: str, port: int) -> None:
    """Start the browser."""
    profile_dir = tempfile.mkdtemp(prefix=f"webgui{uuid.uuid4().hex}")

    url = f"http://{address}:{port}"

    browser_path_dispacher = {
        "windows": find_browser_on_windows,
        "linux": find_browser_on_linux,
    }
    browser_path = browser_path_dispacher.get(operating_sys)()
    browser_command = make_browser_command(browser_path, url, profile_dir)
    browser_process = subprocess.Popen(browser_command)  # noqa: S603
    browser_process.wait()
    shutil.rmtree(profile_dir, ignore_errors=True)

    if isinstance(server_process, Process):
        server_process.kill()
    else:
        kill_port(port)


def run_desktop(app: Flask, address: str, port: int, workers: int) -> None:
    """Run the application in a desktop environment."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        server_future = executor.submit(wsgi_server, app, address, port, workers)
        browser_future = executor.submit(start_browser, server_future, address, port)
        try:
            server_future.result()
            browser_future.result()
        except KeyboardInterrupt:
            executor.shutdown()
