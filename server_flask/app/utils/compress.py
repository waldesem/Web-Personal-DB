"""Compressor module."""

from __future__ import annotations

import functools
import gzip
import zlib
from collections import defaultdict
from functools import lru_cache

from flask import Flask, Response, after_this_request, current_app, request


@lru_cache(maxsize=128)
def _choose_algorithm(enabled_algorithms: tuple, accept_encoding: str) -> None | tuple:  # noqa: C901
    """Determine which compression algorithm used based on the client request.

    Args:
        enabled_algorithms: Tuple of supported compression algorithms.
        accept_encoding: Content of the `Accept-Encoding` header.

    Return:
        name of a compression algorithm (`gzip`, `deflate`, `br`, 'zstd')
        or `None` if the client and server don't agree on any.

    """
    # A flag denoting that client requested using any (`*`) algorithm,
    # in case a specific one is not supported by the server
    fallback_to_any = False

    # Map quality factors to requested algorithm names.
    algos_by_quality = defaultdict(set)

    # Set of supported algorithms
    server_algos_set = set(enabled_algorithms)

    for chunk in accept_encoding.lower().split(","):
        part = chunk.strip()
        if ";q=" in part:
            # If the client associated a quality factor with an algorithm, parse it.
            algo = part.split(";")[0].strip()
            try:
                quality = float(part.split("=")[1].strip())
            except ValueError:
                quality = 1.0
        else:
            # Otherwise, use the default quality
            algo = part
            quality = 1.0

        if algo == "*":
            if quality > 0:
                fallback_to_any = True
        elif algo == "identity":  # identity means 'no compression asked'
            algos_by_quality[quality].add(None)
        elif algo in server_algos_set:
            algos_by_quality[quality].add(algo)

    # Choose the algorithm with the highest quality factor that the server supports.
    for _, viable_algos in sorted(algos_by_quality.items(), reverse=True):
        if len(viable_algos) == 1:
            return viable_algos.pop()
        if server_algo := list(filter(lambda x: x in viable_algos, viable_algos)):
            return server_algo[0]

    if fallback_to_any:
        return enabled_algorithms[0]
    return None


class Compress:
    """The Compress object."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init Flask-Compress.

        Args:
            app: the Flask application object or None.

        Returns:
            Nome.

        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Init app."""
        defaults = [
            (
                "COMPRESS_MIMETYPES",
                [
                    "text/html",
                    "text/css",
                    "text/plain",
                    "text/xml",
                    "text/x-component",
                    "text/javascript",  # Obsolete (RFC 9239)
                    "application/x-javascript",
                    "application/javascript",
                    "application/json",
                    "application/manifest+json",
                    "application/vnd.api+json",
                    "application/xml",
                    "application/xhtml+xml",
                    "application/rss+xml",
                    "application/atom+xml",
                    "application/vnd.ms-fontobject",
                    "application/x-font-ttf",
                    "application/x-font-opentype",
                    "application/x-font-truetype",
                    "image/svg+xml",
                    "image/x-icon",
                    "image/vnd.microsoft.icon",
                    "font/ttf",
                    "font/eot",
                    "font/otf",
                    "font/opentype",
                ],
            ),
            ("COMPRESS_LEVEL", 6),
            ("COMPRESS_DEFLATE_LEVEL", -1),
            ("COMPRESS_MIN_SIZE", 500),
            ("COMPRESS_CACHE_KEY", None),
            ("COMPRESS_CACHE_BACKEND", None),
            ("COMPRESS_REGISTER", True),
            ("COMPRESS_STREAMS", True),
            ("COMPRESS_ALGORITHM", ["gzip", "deflate"]),
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        backend = app.config["COMPRESS_CACHE_BACKEND"]
        self.cache = backend() if backend else None
        self.cache_key = app.config["COMPRESS_CACHE_KEY"]

        self.compress_mimetypes_set = set(app.config["COMPRESS_MIMETYPES"])

        algo = app.config["COMPRESS_ALGORITHM"]
        if isinstance(algo, str):
            self.enabled_algorithms = tuple(i.strip() for i in algo.split(","))
        else:
            self.enabled_algorithms = tuple(algo)

        if app.config["COMPRESS_REGISTER"] and app.config["COMPRESS_MIMETYPES"]:
            app.after_request(self.after_request)

    def after_request(self, response: Response) -> None:
        """Make after request."""
        app = self.app or current_app

        vary = response.headers.get("Vary")
        if not vary:
            response.headers["Vary"] = "Accept-Encoding"
        elif "accept-encoding" not in vary.lower():
            response.headers["Vary"] = f"{vary}, Accept-Encoding"

        accept_encoding = request.headers.get("Accept-Encoding", "")
        chosen_algorithm = _choose_algorithm(self.enabled_algorithms, accept_encoding)

        if (
            chosen_algorithm is None
            or response.mimetype not in self.compress_mimetypes_set
            or response.status_code < 200
            or response.status_code >= 300
            or (response.is_streamed and app.config["COMPRESS_STREAMS"] is False)
            or "Content-Encoding" in response.headers
            or (
                response.content_length is not None
                and response.content_length < app.config["COMPRESS_MIN_SIZE"]
            )
        ):
            return response

        response.direct_passthrough = False

        if self.cache is not None:
            key = f"{chosen_algorithm};{self.cache_key(request)}"
            compressed_content = self.cache.get(key)
            if compressed_content is None:
                compressed_content = self.compress(app, response, chosen_algorithm)
            self.cache.set(key, compressed_content)
        else:
            compressed_content = self.compress(app, response, chosen_algorithm)

        response.set_data(compressed_content)

        response.headers["Content-Encoding"] = chosen_algorithm
        response.headers["Content-Length"] = response.content_length

        etag = response.headers.get("ETag")
        if etag:
            response.headers["ETag"] = f'{etag[:-1]}:{chosen_algorithm}"'

        return response

    def compressed(self) -> None:
        """Compress."""

        def decorator(f: callable) -> callable:
            """Decorate."""

            @functools.wraps(f)
            def decorated_function(*args: tuple, **kwargs: dict) -> callable:
                @after_this_request
                def compressor(response: Response) -> callable:
                    return self.after_request(response)

                return f(*args, **kwargs)

            return decorated_function

        return decorator

    def compress(self, app: Flask, response: Response, algorithm: str) -> bytes:
        """Compress response data."""
        if algorithm == "deflate":
            return zlib.compress(
                response.get_data(),
                app.config["COMPRESS_DEFLATE_LEVEL"],
            )
        return gzip.compress(
            response.get_data(),
            app.config["COMPRESS_LEVEL"],
        )
