from app import create_app

# import eventlet
# from eventlet import wsgi

# from gevent.pywsgi import WSGIServer


app = create_app()


if __name__ == '__main__':
    app.run()  # Start WSGI server with sync workers

    # wsgi.server(eventlet.listen(("127.0.0.1", 8000)), app)  # Start WSGI server with eventlet workers

    # http_server = WSGIServer(("127.0.0.1", 8000), app)  # Start WSGI server with gevent workers
    # http_server.serve_forever()
