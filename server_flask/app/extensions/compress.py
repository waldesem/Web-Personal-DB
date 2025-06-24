"""Compression module.

Original code - https://github.com/colour-science/flask-compress
"""

from __future__ import annotations

import gzip

from flask import Flask, Response, request


class DictCache:
    """Dict Cache."""

    def __init__(self) -> None:
        """Init cache."""
        self.data = {}

    def get(self, key: str) -> str:
        """Get cache key."""
        return self.data.get(key)

    def set(self, key: str, value: Response) -> None:
        """Set cache value."""
        self.data[key] = value


class Compress:
    """The Compress object allows your application."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init class."""
        if app is not None:
            self.init_app(app)
        self.cache = DictCache()
        self.cache_key = None

    def init_app(self, app: Flask) -> None:
        """Init app."""
        app.after_request(self.after_request)

    def after_request(self, response: Response) -> Response:
        """After request."""
        # Compress the response if possible.
        vary = response.headers.get("Vary")
        if not vary:
            response.headers["Vary"] = "Accept-Encoding"
        elif "accept-encoding" not in vary.lower():
            response.headers["Vary"] = f"{vary}, Accept-Encoding"

        # Only compress text/* and application/json content types.
        if (
            not response.mimetype.startswith(("text/", "application/json"))
            or response.status_code < 200
            or response.status_code >= 300
            or "Content-Encoding" in response.headers
            or (response.content_length is not None and response.content_length < 1000)
        ):
            return response

        response.direct_passthrough = False

        if response.mimetype.startswith("text/"):
            key = f"{self.cache_key(request.url)}"
            compressed_content = self.cache.get(key)
            if compressed_content is None:
                compressed_content = gzip.compress(response.get_data())
            self.cache.set(key, compressed_content)
        else:
            compressed_content = gzip.compress(response.get_data())

        response.set_data(compressed_content)

        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = response.content_length
        return response
