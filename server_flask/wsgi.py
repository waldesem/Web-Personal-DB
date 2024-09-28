from concurrent.futures import ThreadPoolExecutor

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi


def wsgi_server(app, address, port, workers):
    """
    Start a WSGI server using Tornado.

    :param app: A WSGI application object
    :param address: The address to listen on
    :param port: The port to listen on
    :param workers: The number of worker threads to use
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
