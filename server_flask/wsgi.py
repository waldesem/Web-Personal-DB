"""WSGI server using Tornado."""

from flask import Flask
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer


def wsgi_server(app: Flask, address: str, port: int) -> None:
    """Start a WSGI server using Tornado."""
    container = WSGIContainer(app)
    http_server = HTTPServer(container)
    http_server.listen(port, address)
    loop = IOLoop.current()
    try:
        print(f"Listening on http://{address}:{port}")  # noqa: T201
        loop.start()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
