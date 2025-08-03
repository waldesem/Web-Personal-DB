"""WSGI server using Tornado."""

from concurrent.futures import ThreadPoolExecutor

from flask import Flask
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer


def wsgi_server(app: Flask, address: str, port: int, workers: int) -> None:
    """Start a WSGI server using Tornado."""
    container = WSGIContainer(app)
    http_server = HTTPServer(container)
    http_server.listen(port, address)
    executor = ThreadPoolExecutor(max_workers=workers)
    loop = IOLoop.current()
    loop.set_default_executor(executor)
    try:
        print(f"Listening on http://{address}:{port}")  # noqa: T201
        loop.start()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
        executor.shutdown(wait=True)
