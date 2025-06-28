"""Compression module.

Original code - https://github.com/colour-science/flask-compress
"""

from __future__ import annotations

import gzip

from flask import Flask, Response  # noqa: TC002


class Compress:
    """The Compress object allows your application."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init class."""
        if app is not None:
            self.init_app(app)

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

        compressed_content = gzip.compress(response.get_data())
        response.set_data(compressed_content)

        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = response.content_length
        return response
