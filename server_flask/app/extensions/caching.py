"""Caching module."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any


class Cache:
    """A simple cache database.

    data = {
        "1": {
            "persons": "",
            "staffs": [],
            ...,
        },
    }
    """

    def __init__(self) -> None:
        """Initialize the database."""
        self.data: OrderedDict[str, dict[str, Any]] = OrderedDict()

    def get_data(self, person_id: int, item: str) -> str | list:
        """Get the value of a keys."""
        try:
            values = self.data[f"{person_id}"]
            self.data.move_to_end(f"{person_id}")
            return values[item]
        except KeyError:
            return None

    def set_data(self, person_id: int, item: str, value: str | list) -> None:
        """Set the value of a key."""
        if f"{person_id}" not in self.data:
            self.pop_data()
            self.data[f"{person_id}"] = {}
        self.data[f"{person_id}"][item] = value

    def delete_data(self, person_id: int) -> None:
        """Clear the data."""
        if f"{person_id}" in self.data:
            del self.data[f"{person_id}"]

    def pop_data(self) -> None:
        """Check old data."""
        if len(self.data) > 99:
            self.data.popitem(last=False)
