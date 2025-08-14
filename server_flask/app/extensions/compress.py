"""Compression module."""

from __future__ import annotations

import zlib

from flask import Flask, Response  # noqa: TC002


class Compress:
    """The Compress object allows your application."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init class."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Init app."""
        app.after_request(self._after_request)

    def _after_request(self, response: Response) -> Response:
        """After request."""
        # Compress the response if possible.
        if not (vary := response.headers.get("Vary")):
            response.headers["Vary"] = "Accept-Encoding"
        elif "accept-encoding" not in vary.lower():
            response.headers["Vary"] = f"{vary}, Accept-Encoding"

        # Only compress application/json and text/* content types.
        if (
            (
                "/json" not in response.mimetype
                and "text/" not in response.content_type
            )
            or 200 > response.status_code >= 300
            or "Content-Encoding" in response.headers
            or (response.content_length is not None and response.content_length < 1000)
        ):
            return response

        response.direct_passthrough = False
        compressed_content = zlib.compress(response.get_data())
        response.set_data(compressed_content)

        response.headers["Content-Encoding"] = "deflate"
        response.headers["Content-Length"] = response.content_length
        return response
