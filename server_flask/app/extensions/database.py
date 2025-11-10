"""Database extension."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

if TYPE_CHECKING:
    from flask import Flask


class Base(DeclarativeBase):
    """Base class for models."""


class Database:
    """The Database object allows your application."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init class."""
        self.Model = Base
        self.metadata = self.Model.metadata
        self.metatables = self.metadata.tables
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Init app."""
        if not app.config["DATABASE_URI"]:
            msg = "DATABASE_URI is Empty."
            raise RuntimeError(msg)

        self.engine = create_engine(app.config["DATABASE_URI"])
        if not self.metatables:
            self.metadata.create_all(bind=self.engine)
        self.session = scoped_session(
            sessionmaker(bind=self.engine, autoflush=False, autocommit=False),
        )

        app.teardown_appcontext(self._teardown_session)

    def _teardown_session(self, exc: BaseException | None = None) -> None:  # noqa: ARG002
        """Close the database session after each request."""
        self.session.remove()
