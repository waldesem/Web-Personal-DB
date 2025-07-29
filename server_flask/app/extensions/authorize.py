"""A simple database for JWT tokens."""

from __future__ import annotations

from datetime import datetime, timezone

import jwt
from flask import Flask, current_app, g, request
from pydantic import ValidationError

from app.models.models import Token


class RevokeDB:
    """A simple database for JWT tokens."""

    def __init__(self) -> None:
        """Initialize the database."""
        if not hasattr(self, "data"):
            self.data = {}
        else:
            self.data = self.data

    def get(self, key: str) -> str:
        """Get the value of a key."""
        return self.data.get(key)

    def set(self, key: str, value: str) -> None:
        """Set the value of a key."""
        self.data[key] = value

    def delete(self, key: str) -> None:
        """Delete a key."""
        if self.get(key):
            del self.data[key]

    def clear(self) -> None:
        """Clear the database."""
        self.data.clear()


class Auth:
    """A simple jwt authorization class."""

    def __init__(self, app: Flask | None = None) -> None:
        """Initialize the database."""
        if app is not None:
            self.init_app(app)
        self.jwt_revoked_db = RevokeDB()

    def init_app(self, app: Flask) -> None:
        """Register the before_request handler."""
        app.before_request(self._before_request)

    def _before_request(self) -> None:
        """Authenticate user via JWT and populate g.token."""
        if (
            (header := request.headers.get("Authorization"))
            and (token := self._decode_token(header[7:]))
            and token.jti not in self.jwt_revoked_db.data
        ):
            g.token = token.dict()

    def revoke_token(self) -> None:
        """Revoke the current token and delete expired tokens from db."""
        self.jwt_revoked_db.set(g.token["jti"], g.token["exp"])
        for key, value in self.jwt_revoked_db.data.items():
            if value < datetime.now(tz=timezone.utc):
                self.jwt_revoked_db.delete(key)

    @staticmethod
    def _decode_token(payload: str) -> Token | None:
        """Decode JWT token and return payload."""
        try:
            decoded = jwt.decode(
                payload,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
                options={"verify_exp": True},
            )
            token = Token(**decoded)
        except (jwt.exceptions.PyJWTError, ValidationError):
            current_app.logger.exception("JWT decode failed")
            return None
        else:
            return token
