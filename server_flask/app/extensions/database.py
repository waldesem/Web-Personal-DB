"""Database extension."""

from __future__ import annotations

from typing import Optional, TypedDict

from flask import Flask, current_app
from sqlalchemy import MetaData, Select, Sequence, create_engine, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker


class Base(DeclarativeBase):
    """Base class for models."""

    def to_dict(self) -> dict:
        """Convert model to dict."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Paging(TypedDict, total = False):
    """Pagination class."""

    total: int
    query: Sequence


class Database:
    """The Database object allows your application."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init class."""
        self.Model = Base
        self.metadata = None
        self.session = Optional[Session]
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Init app."""
        if not app.config["DATABASE_URI"]:
            msg = "DATABASE_URI is Empty."
            raise RuntimeError(msg)

        engine = create_engine(app.config["DATABASE_URI"])
        self.metadata = Base.metadata
        self.metadata.create_all(bind=engine)
        self.session = scoped_session(
            sessionmaker(bind=engine, autoflush=False, autocommit=False),
        )

        app.teardown_appcontext(self._teardown_session)

    def _teardown_session(self, exc: BaseException | None = None) -> None:  # noqa: ARG002
        """Close the database session after each request."""
        self.session.remove()

    @property
    def metatables(self) -> MetaData:
        """The default metadata."""
        return self.metadata.tables

    def paginate(self, stmt: Select, page: int = 1, per_page: int = 10) -> Paging:
        """Paginate query."""
        paging = Paging()
        try:
            # Получаем параметры пагинации из запроса
            page = max(page, 1)
            per_page = max(per_page, 1)

            # Получаем общее количество записей
            paging["total"] = self.session.execute(
                select(func.count()).select_from(stmt),
            ).scalar()
            # Получаем данные для текущей страницы
            query = self.session.execute(
                stmt.offset(
                    (page - 1) * per_page,
                ).limit(per_page),
            ).all()
            # Преобразуем данные в список словарей
            paging["query"] = [row._asdict() for row in query]
        except (SQLAlchemyError, TypeError):
            current_app.logger.exception("Pagination Error")
        # Возвращаем словарь с данными пагинации и данными для текущей страницы
        return paging
