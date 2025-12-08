"""Compression module."""

from __future__ import annotations

import typing
import zlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask, Response


class Compress:
    """The Compress object allows your application."""

    mimetypes: typing.ClassVar = [
        "application/dash+xml",
        "application/eot",
        "application/font",
        "application/font-sfnt",
        "application/javascript",
        "application/json",
        "application/opentype",
        "application/otf",
        "application/pdf",
        "application/pkcs7-mime",
        "application/protobuf",
        "application/rss+xml",
        "application/truetype",
        "application/ttf",
        "application/vnd.apple.mpegurl",
        "application/vnd.mapbox-vector-tile",
        "application/vnd.ms-fontobject",
        "application/wasm",
        "application/xhtml+xml",
        "application/xml",
        "application/x-font-opentype",
        "application/x-font-truetype",
        "application/x-font-ttf",
        "application/x-httpd-cgi",
        "application/x-javascript",
        "application/x-mpegurl",
        "application/x-opentype",
        "application/x-otf",
        "application/x-perl",
        "application/x-ttf",
        "font/eot",
        "font/opentype",
        "font/otf",
        "font/ttf",
        "image/svg+xml",
        "text/css",
        "text/csv",
        "text/html",
        "text/javascript",
        "text/js",
        "text/plain",
        "text/richtext",
        "text/tab-separated-values",
        "text/xml",
        "text/x-component",
        "text/x-java-source",
        "text/x-script",
        "vnd.apple.mpegurl",
    ]

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
            response.mimetype in self.mimetypes
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
