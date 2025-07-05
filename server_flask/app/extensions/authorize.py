"""A simple database for JWT tokens."""

from __future__ import annotations

import jwt
from flask import Flask, current_app, g, request
from pydantic import ValidationError

from app.extensions.simpedb import SimpleDB
from app.structures.models import Token


class JwtAuth:
    """A simple jwt authorization class."""

    def __init__(self, app: Flask | None = None) -> None:
        """Initialize the database."""
        if app is not None:
            self.init_app(app)
        self.token = None
        self.jwt_revoked_db = SimpleDB()

    def init_app(self, app: Flask) -> None:
        """Register the before_request handler."""
        app.before_request(self._before_request)

    def _before_request(self) -> None:
        """Authenticate user via JWT and populate g.user_id."""
        g.user_id = None
        if header := request.headers.get("Authorization"):
            token = self._decode_token(header[7:])
            if token:
                self.token = token
                g.user_id = token.id

    def _decode_token(self, payload: str) -> Token | None:
        """Decode JWT token and return payload."""
        try:
            decoded = jwt.decode(
                payload,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
                options={"verify_exp": True},
            )
            token = Token(**decoded)
            if token.jti in self.jwt_revoked_db.data:
                return None
        except (jwt.exceptions.PyJWTError, ValidationError):
            current_app.logger.exception("JWT decode failed")
            return None
        else:
            return token
