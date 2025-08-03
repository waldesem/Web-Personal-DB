"""WebGUI module.

Original code - https://github.com/ClimenteA/flaskwebgui
"""

from __future__ import annotations

import shutil
import signal
import subprocess
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psutil
from flask import Flask  # noqa: TC002


def start_browser(address: str, port: int) -> None:
    """Start the browser."""
    profile_dir = tempfile.mkdtemp(prefix=f"webgui{uuid.uuid1().hex}")
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]

    if browser_paths := list(filter(lambda path: Path(path).is_file(), paths)):
        subprocess.Popen(  # noqa: S603
            [
                browser_paths[0],
                f"--app=http://{address}:{port}",
                f"--user-data-dir={profile_dir}",
                "--new-window",
                "--no-default-browser-check",
                "--no-first-run",
                "--window-size=1280,960",
            ],
        ).wait()

    shutil.rmtree(profile_dir, ignore_errors=True)
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                psutil.Process(conn.pid).send_signal(signal.SIGTERM)
            except psutil.AccessDenied:
                continue
            break


def run_desktop(app: Flask, address: str, port: int) -> None:
    """Run the application in a desktop environment."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        server_future = executor.submit(app.run, address, port)
        browser_future = executor.submit(start_browser, address, port)
        try:
            server_future.result()
            browser_future.result()
        except KeyboardInterrupt:
            executor.shutdown()
