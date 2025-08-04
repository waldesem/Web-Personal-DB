"""WSGI server using Tornado."""

import asyncio

from flask import Flask
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer


async def async_server(app: Flask, address: str, port: int) -> None:
    """Start a WSGI server using Tornado."""
    container = WSGIContainer(app)
    http_server = HTTPServer(container)
    http_server.listen(port, address)
    try:
        print(f"Listening on http://{address}:{port}")  # noqa: T201
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        asyncio.get_event_loop().stop()
