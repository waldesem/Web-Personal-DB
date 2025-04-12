"""WSGI server using Tornado."""

from concurrent.futures import ThreadPoolExecutor

from flask import Flask
from tornado import httpserver, ioloop, wsgi


def wsgi_server(app: Flask, address: str, port: int, workers: int) -> None:
    """Start a WSGI server using Tornado.

    :param app: A WSGI application object
    :param address: The address to listen on
    :param port: The port to listen on
    :param workers: The number of worker threads to use
    """
    container = wsgi.WSGIContainer(app)
    http_server = httpserver.HTTPServer(container)
    http_server.listen(port, address)
    executor = ThreadPoolExecutor(max_workers=workers)
    loop = ioloop.IOLoop.current()
    loop.set_default_executor(executor)
    try:
        print(f"Listening on http://{address}:{port}")  # noqa: T201
        loop.start()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
        executor.shutdown(wait=True)
