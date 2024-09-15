import asyncio
from concurrent.futures import ThreadPoolExecutor

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi


async def tornado_server(app, address, port):
    container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port, address)
    executor = ThreadPoolExecutor(max_workers=8)
    loop = tornado.ioloop.IOLoop.current()
    loop.set_default_executor(executor)
    await asyncio.Event().wait()


def wsgi_server(app, address="127.0.0.1", port=5000):
    asyncio.run(tornado_server(app, address, port))
