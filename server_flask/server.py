"""A module that runs the application server."""

import argparse
import asyncio

from app import create_app
from webgui import run_desktop
from wsgi import async_server


def main() -> None:
    """Run the application server based on the provided arguments.

    Example usage:
        For debugging:
            uv run server.py --host 127.0.0.1 --port 5000 --mode debug

        For development:
            uv run server.py --host 127.0.0.1 --port 5000 --mode devel

        For production:
            uv run server.py --host 127.0.0.1 --port 5000 --mode server

        For desktop:
            uv run server.py
    """
    parser = argparse.ArgumentParser(description="Run the application server.")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="The host to bind the server to.",
    )
    parser.add_argument(
        "--port",
        default=5000,
        type=int,
        help="The port to run the server on.",
    )
    parser.add_argument(
        "--mode",
        choices=["debug", "devel", "async", "desktop"],
        default="desktop",
        help="The mode to run the server in (debug, devel, async, desktop).",
    )
    args = parser.parse_args()

    app = create_app()

    match args.mode:
        case "debug":
            app.run(host=args.host, port=args.port, debug=True)
        case "devel":
            app.run(host=args.host, port=args.port, debug=False)
        case "async":
            asyncio.run(async_server(app, address=args.host, port=args.port))
        case _:
            run_desktop(app, address=args.host, port=args.port)


if __name__ == "__main__":
    main()
