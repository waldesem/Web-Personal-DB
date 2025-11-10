"""Compression module."""

from __future__ import annotations

import zlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask, Response


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

        # Only compress */json and text/* content types.
        if (
            (
                (response.mimetype and "/json" in response.mimetype)
                or "text/" in response.content_type
            )
            and 300 > response.status_code >= 200
            and response.content_length
            and response.content_length > 1000
        ):
            response.direct_passthrough = False
            compressed_content = zlib.compress(response.get_data())
            response.set_data(compressed_content)

            response.headers["Content-Encoding"] = "deflate"
            response.headers["Content-Length"] = response.content_length
            return response
        return response
