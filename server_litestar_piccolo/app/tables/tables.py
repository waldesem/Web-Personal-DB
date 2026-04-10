"""Piccolo database schema."""

from datetime import datetime

from piccolo.columns.base import OnDelete, OnUpdate
from piccolo.columns.column_types import (
    Boolean,
    Bytea,
    Date,
    ForeignKey,
    Integer,
    Serial,
    Text,
    Timestamptz,
    Varchar,
)
from piccolo.columns.defaults.date import DateNow
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.table import Table

from app.classes.classes import Conclusions, Decisions, Roles


class CreateUpdateIdMixin:
    """Create Update Id Mixin."""

    id = Serial(primary_key=True)
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Users(CreateUpdateIdMixin, Table):
    """Table users."""

    fullname = Varchar(length=255)
    username = Varchar(length=255, unique=True, index=True)
    email = Varchar(length=255, unique=True)
    passhash = Bytea(default=b"", secret=True)
    pswd_create = Timestamptz(default=TimestamptzNow())
    change_pswd = Boolean(default=False)
    blocked = Boolean(default=False)
    deleted = Boolean(default=False)
    attempt = Integer(default=0)
    role = Varchar(length=255, choices=Roles)


class AlembicVersion(Table, tablename="alembic_version"):
    """Table alembic_version."""

    version_num = Varchar(length=32, primary_key=True, index=True)


class Persons(CreateUpdateIdMixin, Table):
    """Table persons."""

    surname = Varchar(length=255)
    firstname = Varchar(length=255)
    patronymic = Varchar(length=255, null=True)
    birthday = Date(default=DateNow())
    birthplace = Varchar(length=255, null=True)
    citizenship = Varchar(length=255, null=True)
    dual = Varchar(length=255, null=True)
    snils = Varchar(length=11, null=True)
    inn = Varchar(length=12, null=True)
    marital = Varchar(length=255, null=True)
    addition = Text(null=True)
    destination = Text(null=True)
    user_id = ForeignKey(references=Users)


class ItemMixin(CreateUpdateIdMixin):
    """Item Mixin."""

    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )


class Addresses(ItemMixin, Table, tags=["addresses"]):
    """Table addresses."""

    view = Varchar(length=255)
    address = Varchar(length=255)


class Affilations(ItemMixin, Table, tags=["affilations"]):
    """Table affilations."""

    view = Varchar(length=255)
    organization = Varchar(length=255)
    inn = Varchar(length=255, null=True)


class Checks(ItemMixin, Table, tags=["checks"]):
    """Table checks."""

    workplace = Text(null=True)
    document = Text(null=True)
    inn = Text(null=True)
    debt = Text(null=True)
    bankruptcy = Text(null=True)
    bki = Text(null=True)
    courts = Text(null=True)
    affilation = Text(null=True)
    terrorist = Text(null=True)
    mvd = Text(null=True)
    internet = Text(null=True)
    cronos = Text(null=True)
    cros = Text(null=True)
    addition = Text(null=True)
    comment = Text(null=True)
    conclusion = Varchar(length=255, choices=Conclusions)


class Contacts(ItemMixin, Table, tags=["contacts"]):
    """Table contacts."""

    view = Varchar(length=255)
    contact = Varchar(length=255)


class Documents(ItemMixin, Table, tags=["documents"]):
    """Table documents."""

    view = Varchar(length=255)
    series = Varchar(length=12, null=True)
    digits = Varchar(length=24)
    agency = Varchar(length=255, null=True)
    issue = Date(default=DateNow(), null=True)


class Educations(ItemMixin, Table, tags=["educations"]):
    """Table educations."""

    view = Varchar(length=255, null=True)
    institution = Text(null=False)
    finished = Varchar(length=4, null=True)
    specialty = Varchar(length=255, null=True)


class Inquiries(ItemMixin, Table, tags=["inquiries"]):
    """Table inquiries."""

    info = Text(null=False)
    initiator = Varchar(length=255)


class Investigations(ItemMixin, Table, tags=["investigations"]):
    """Table investigations."""

    theme = Varchar(length=255)
    info = Text(null=False)


class Poligrafs(ItemMixin, Table, tags=["poligrafs"]):
    """Table poligrafs."""

    theme = Varchar(length=255)
    results = Text(null=False)
    conclusion = Varchar(length=255, choices=Decisions)


class Previous(ItemMixin, Table, tags=["previous"]):
    """Table previous."""

    surname = Varchar(length=255)
    firstname = Varchar(length=255, null=True)
    patronymic = Varchar(length=255, null=True)
    changed = Varchar(length=4, null=True)
    reason = Text(null=True)


class Staffs(ItemMixin, Table, tags=["staffs"]):
    """Table staffs."""

    position = Varchar(length=255)
    department = Varchar(length=255, null=True)


class Workplaces(ItemMixin, Table, tags=["workplaces"]):
    """Table workplaces."""

    now_work = Boolean(default=False)
    starts = Date(default=DateNow())
    finished = Date(default=DateNow(), null=True)
    workplace = Varchar(length=255)
    address = Varchar(length=255, null=True)
    position = Varchar(length=255)
    reason = Text(null=True)
