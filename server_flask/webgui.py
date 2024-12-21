"""WebGUI module."""

import platform
import shutil
import signal
import subprocess
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psutil
from flask import Flask

from wsgi import wsgi_server


def find_browser_on_linux() -> str:
    """Find the path to the browser on Linux."""
    paths = ["/snap/bin/chromium", "/snap/bin/firefox"]
    for path in paths:
        if Path(path).exists():
            return path
    return None


def find_browser_on_windows() -> str:
    """Find the path to the browser on Windows."""
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


def start_browser(address: str, port: int) -> None:
    """Start the browser."""
    profile_dir = tempfile.mkdtemp(prefix=f"webgui{uuid.uuid4().hex}")
    browser_path_dispacher = {
        "windows": find_browser_on_windows,
        "linux": find_browser_on_linux,
    }
    browser_path = browser_path_dispacher.get(platform.system().lower())
    if not browser_path:
        browser_process = subprocess.Popen(  # noqa: S603
            [
                browser_path(),
                f"--app=http://{address}:{port}",
                f"--user-data-dir={profile_dir}",
                "--new-window",
                "--no-default-browser-check",
                "--no-first-run",
                "--disable-sync",
                "--disable-extensions",
                "--window-size=1280,960",
            ],
        )
        browser_process.wait()

    shutil.rmtree(profile_dir, ignore_errors=True)
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                psutil.Process(conn.pid).send_signal(signal.SIGTERM)
            except psutil.AccessDenied:
                continue
            break


def run_desktop(app: Flask, address: str, port: int, workers: int) -> None:
    """Run the application in a desktop environment."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        server_future = executor.submit(wsgi_server, app, address, port, workers)
        browser_future = executor.submit(start_browser, address, port)
        try:
            server_future.result()
            browser_future.result()
        except KeyboardInterrupt:
            executor.shutdown()
