"""A simple cache for JWT tokens."""


class JWTCache:
    """A simple cache for JWT tokens."""

    def __init__(self) -> None:
        """Initialize the cache."""
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
        else:
            msg = f"Key '{key}' not found in cache."
            raise KeyError(msg)

    def clear(self) -> None:
        """Clear the cache."""
        if self.data:
            self.data.clear()
        else:
            msg = "Cache is already empty."
            raise ValueError(msg)
