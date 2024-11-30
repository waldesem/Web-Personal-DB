import os
import platform
import shutil
import signal
import subprocess
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

import psutil
from wsgi import wsgi_server


operating_sys = platform.system().lower()


def find_browser_on_linux():
    paths = ["/snap/bin/chromium", "/snap/bin/firefox"]
    for path in paths:
        if os.path.exists(path):
            return path
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


def make_browser_command(browser_path, url, profile_dir):
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


def kill_port(port: int):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                psutil.Process(conn.pid).send_signal(signal.SIGTERM)
            except psutil.AccessDenied:
                continue
            break


def start_browser(server_process, address, port):
    profile_dir = tempfile.mkdtemp(prefix=f"webgui{uuid.uuid4().hex}")

    url = f"http://{address}:{port}"

    browser_path_dispacher = {
        "windows": find_browser_on_windows,
        "linux": find_browser_on_linux,
    }
    browser_path = browser_path_dispacher.get(operating_sys, None)()
    browser_command = make_browser_command(browser_path, url, profile_dir)
    browser_process = subprocess.Popen(browser_command)
    browser_process.wait()
    shutil.rmtree(profile_dir, ignore_errors=True)

    if isinstance(server_process, Process):
        server_process.kill()
    else:
        kill_port(port)


def run_desktop(app, address, port, workers):
    with ThreadPoolExecutor(max_workers=2) as executor:
        server_future = executor.submit(wsgi_server, app, address, port, workers)
        browser_future = executor.submit(start_browser, server_future, address, port)
        try:
            server_future.result()
            browser_future.result()
        except KeyboardInterrupt:
            executor.shutdown()
            print("Stopped")
