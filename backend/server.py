from app import create_app
from waitress import serve
import argparse


def main():
    """
    A function that runs the application server based on the provided arguments.

    Example usage:
        For debugging:
            python server.py --host 127.0.0.1 --port 5000 --actions debug

        For development:
            python server.py --host 127.0.0.1 --port 5000 --actions dev

        For production:
            python server.py --host 127.0.0.1 --port 8000 --actions prod

    """
    parser = argparse.ArgumentParser(description="Run the application server.")
    parser.add_argument(
        "--host", default="127.0.0.1", help="The host to bind the server to."
    )
    parser.add_argument(
        "--port", default=5000, type=int, help="The port to run the server on."
    )
    parser.add_argument(
        "--threads", default=8, type=int, help="The number of threads to use."
    )
    parser.add_argument(
        "--actions",
        choices=["debug", "develop", "prod"],
        default="debug",
        help="The action to run the server in.",
    )
    args = parser.parse_args()

    app = create_app()

    if args.actions == "debug":
        app.run(host=args.host, port=args.port, debug=True)
    elif args.actions == "develop":
        app.run(host=args.host, port=args.port, debug=False)
    else:
        serve(app, host=args.host, port=args.port, threads=8)


if __name__ == "__main__":
    main()
