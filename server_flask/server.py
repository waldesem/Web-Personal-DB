"""A module that runs the application server."""

import argparse

from app import create_app
from simple import simple_wsgi
from webgui import run_desktop
from wsgi import wsgi_server


def main() -> None:
    """Run the application server based on the provided arguments.

    Example usage:
        For debugging:
            python server.py --host 127.0.0.1 --port 5000 --mode debug.
            uv run server.py --host 127.0.0.1 --port 5000 --mode debug

        For development:
            python server.py --host 127.0.0.1 --port 5000 --mode simple
            uv run server.py --host 127.0.0.1 --port 5000 --mode simple

        For production:
            python server.py --host 127.0.0.1 --port 5000 --workers 8 --mode server
            uv run server.py --host 127.0.0.1 --port 5000 --workers 8 --mode server

        For desktop:
            python server.py
            uv run server.py
    """
    parser = argparse.ArgumentParser(description="Run the application server.")
    parser.add_argument(
        "--host", default="127.0.0.1", help="The host to bind the server to.",
    )
    parser.add_argument(
        "--port", default=5000, type=int, help="The port to run the server on.",
    )
    parser.add_argument(
        "--workers", default=8, type=int, help="The number of workers to use.",
    )
    parser.add_argument(
        "--mode",
        choices=["debug", "simple", "server", "desktop"],
        default="desktop",
        help="The mode to run the server in (debug, simple, server, desktop).",
    )
    args = parser.parse_args()

    app = create_app()

    match args.mode:
        case "debug":
            app.run(host=args.host, port=args.port, debug=True)
        case "simple":
            simple_wsgi(app, address=args.host, port=args.port)
        case "server":
            wsgi_server(app, address=args.host, port=args.port, workers=args.workers)
        case _:
            run_desktop(app, address=args.host, port=args.port)


if __name__ == "__main__":
    main()
