"""Database extension."""

from __future__ import annotations

from flask import Flask  # noqa: TC002
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker


class Base(DeclarativeBase):
    """Base class for models."""

    def to_dict(self) -> dict:
        """Convert model to dict."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Database:
    """The Database object allows your application."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init class."""
        self.Model = Base
        self.metadatas = None
        self.session = None | Session
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Init app."""
        if not app.config["DATABASE_URI"]:
            msg = "DATABASE_URI is Empty."
            raise RuntimeError(msg)

        engine = create_engine(app.config["DATABASE_URI"])

        self.metadatas = Base.metadata

        self.metadatas.create_all(bind=engine)

        self.session = scoped_session(
            sessionmaker(bind=engine, autoflush=False, autocommit=False),
        )

        app.teardown_appcontext(self._teardown_session)

    def _teardown_session(self, exc: BaseException | None = None) -> None:  # noqa: ARG002
        """Close the database session after each request."""
        self.session.remove()

    @property
    def metadata(self) -> MetaData:
        """The default metadata if no bind key is set."""
        return self.metadatas.tables[None]
