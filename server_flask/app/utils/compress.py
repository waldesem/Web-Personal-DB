"""Compress module.

Original code - https://github.com/colour-science/flask-compress
"""

from __future__ import annotations

import gzip
import zlib
from collections import defaultdict
from functools import lru_cache

from flask import Flask, Response, current_app, request


class DictCache:
    """Dict Cache."""

    def __init__(self) -> None:
        """Init."""
        self.data = {}

    def get(self, key: str) -> None:
        """Getter."""
        return self.data.get(key)

    def set(self, key: str, value: bytes | None) -> None:
        """Setter."""
        self.data[key] = value


@lru_cache(maxsize=64)
def _choose_algorithm(algorithms: tuple, encoding: str) -> str:  # noqa: C901, PLR0912
    """Determine which compression algorithm to use based on the client request.

    The `Accept-Encoding` header may list one or more desired
    algorithms, together with a "quality factor" for each one (higher quality
    means the client prefers that algorithm more).

    :param enabled_algorithms: Tuple of supported compression algorithms
    :param accept_encoding: Content of the `Accept-Encoding` header
    :return: name of a compression algorithm (`gzip`, `deflate`)
        or `None` if the client and server don't agree on any.
    """
    # A flag denoting that client requested using any (`*`) algorithm,
    # in case a specific one is not supported by the server
    fallback_to_any = False

    # Map quality factors to requested algorithm names.
    algos_by_quality = defaultdict(set)

    # Set of supported algorithms
    server_algos_set = set(algorithms)

    for chunk in encoding.lower().split(","):
        part = chunk.strip()
        if ";q=" in part:
            # If the client associated a quality factor with an algorithm,
            # try to parse it. We could do the matching using a regex, but
            # the format is so simple that it would be overkill.
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
    #
    # If there are multiple equally good options,
    # choose the first supported algorithm from server configuration.
    #
    # If the server doesn't support any algorithm that the client requested but
    # there's a special wildcard algorithm request (`*`), choose the first supported
    # algorithm.
    for _, viable_algos in sorted(algos_by_quality.items(), reverse=True):
        if len(viable_algos) == 1:
            return viable_algos.pop()
        for server_algo in algorithms:
            if server_algo in viable_algos:
                return server_algo

    if fallback_to_any:
        return algorithms[0]
    return None


class Compress:
    """The Compress object allows your application to use Flask-Compress.

    When initialising a Compress object you may optionally provide your
    :class:`flask.Flask` application object if it is ready. Otherwise,
    you may provide it later by using the :meth:`init_app` method.

    :param app: optional :class:`flask.Flask` application object
    :type app: :class:`flask.Flask` or None
    """

    def __init__(self, app: Flask | None = None) -> None:
        """Init Class."""
        """An alternative way to pass your :class:`flask.Flask` application
        object to Flask-Compress. :meth:`init_app` also takes care of some
        default `settings`_.

        :param app: the :class:`flask.Flask` application object.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask | None) -> None:
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

    def after_request(self, response: Response) -> Response:
        """After response."""
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

        # "123456789"   => "123456789:gzip"   - A strong ETag validator
        # W/"123456789" => W/"123456789:gzip" - A weak ETag validator
        etag = response.headers.get("ETag")
        if etag:
            response.headers["ETag"] = f'{etag[:-1]}:{chosen_algorithm}"'

        return response

    def compress(self, app: Flask, response: Response, algorithm: str) -> bytes:
        """Compress response."""
        if algorithm == "deflate":
            return zlib.compress(
                response.get_data(), app.config["COMPRESS_DEFLATE_LEVEL"],
            )
        return gzip.compress(
            response.get_data(),
            app.config["COMPRESS_LEVEL"],
        )
