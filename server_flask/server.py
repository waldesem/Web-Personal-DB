"""A module that runs the application server."""

import click

from app import create_app


@click.command("server")
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="The host to bind the server to.",
)
@click.option(
    "--port",
    type=int,
    default=5000,
    help="The port to run the server on.",
)
@click.option(
    "--mode",
    type=click.Choice(["debug", "devel", "desktop"]),
    default="desktop",
    help="The mode to run the server in (debug, devel, desktop).",
)
def server(host: str, port: int, mode: str) -> None:
    """Run the application server based on the provided arguments.

    Example usage:
        For debugging:
            uv run server.py --host 127.0.0.1 --port 5000 --mode debug

        For development:
            uv run server.py --host 127.0.0.1 --port 5000 --mode devel

        For desktop:
            uv run server.py

        For production:
            gunicorn wsgi:app
    """
    app = create_app()

    match mode:
        case "debug":
            app.run(host=host, port=port, debug=True)
        case "devel":
            app.run(host=host, port=port, debug=False)
        case _:
            from webgui import run_desktop

            run_desktop(app, address=host, port=port)


if __name__ == "__main__":
    server()
