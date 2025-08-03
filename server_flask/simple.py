"""Simple WSGI server."""

from wsgiref.simple_server import make_server

from flask import Flask


def simple_wsgi(app: Flask, address: str, port: int) -> None:
    """Start a simple WSGI server using WSGIRef."""
    httpd = make_server(address, port, app)
    try:
        print(f"Listening on http://{address}:{port}")  # noqa: T201
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
