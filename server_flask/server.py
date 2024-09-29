import argparse

from app import create_app
from webgui import FlaskUI
from wsgi import wsgi_server


def main():
    """
    A function that runs the application server based on the provided arguments.
    You also need to check config.py for configuration class.
    Example usage:
        For debugging:
            python server.py --host 127.0.0.1 --port 5000 --mode debug

        For development:
            python server.py --host 127.0.0.1 --port 5000 --mode devel

        For production:
            python server.py --host 127.0.0.1 --port 5000 --workers 8 --mode serve

        For desktop:
            python server.py
    """
    parser = argparse.ArgumentParser(description="Run the application server.")
    parser.add_argument(
        "--host", default="127.0.0.1", help="The host to bind the server to."
    )
    parser.add_argument(
        "--port", default=5000, type=int, help="The port to run the server on."
    )
    parser.add_argument(
        "--workers", default=8, type=int, help="The number of workers to use."
    )
    parser.add_argument(
        "--mode",
        choices=["debug", "devel", "serve", "desktop"],
        default="desktop",
        help="The mode to run the server in (debug, devel, serve, desktop).",
    )
    args = parser.parse_args()

    app = create_app()

    if args.mode == "debug":
        app.run(host=args.host, port=args.port, debug=True)
    elif args.mode == "devel":
        app.run(host=args.host, port=args.port, debug=False)
    elif args.mode == "serve":
        wsgi_server(app, address=args.host, port=args.port, workers=args.workers)
    else:
        FlaskUI(
            server_kwargs={"app": app, "address": args.host, "port": args.port, "workers": args.workers},
        ).run()


if __name__ == "__main__":
    main()
