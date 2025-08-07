"""A simple database for JWT tokens."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import g


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

    def revoke(self) -> None:
        """Revoke the current token and delete expired tokens from db."""
        self.set(g.token["jti"], g.token["exp"])
        for key, value in self.data.items():
            if value < datetime.now(tz=timezone.utc):  # noqa: UP017
                self.delete(key)
