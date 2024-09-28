from concurrent.futures import ThreadPoolExecutor

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi


def wsgi_server(app, address="127.0.0.1", port=5000, workers=8):
    """
    Runs a WSGI application using the Tornado webserver.

    :param app: The WSGI application to run.
    :param address: The address to listen on. Defaults to 127.0.0.1.
    :param port: The port to listen on. Defaults to 5000.
    """
    container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port, address)
    executor = ThreadPoolExecutor(max_workers=workers)
    loop = tornado.ioloop.IOLoop.current()
    loop.set_default_executor(executor)
    try:
        loop.start()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
