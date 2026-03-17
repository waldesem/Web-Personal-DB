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


class Users(Table, tablename="users"):
    """Table users."""

    id = Serial(primary_key=True, index=True)
    fullname = Varchar(length=255)
    username = Varchar(length=255, unique=True, index=True)
    email = Varchar(length=255, unique=True)
    passhash = Bytea(default=b"", secret=True)
    pswd_create = Timestamptz(default=TimestamptzNow())
    change_pswd = Boolean(default=False)
    blocked = Boolean(default=False)
    deleted = Boolean(default=False)
    attempt = Integer(default=0)
    role = Varchar(length=255)
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class AlembicVersion(Table, tablename="alembic_version"):
    """Table alembic_version."""

    version_num = Varchar(length=32, primary_key=True, index=True)


class Persons(Table, tablename="persons"):
    """Table persons."""

    id = Serial(primary_key=True, unique=True)
    surname = Varchar(length=255, index=True)
    firstname = Varchar(length=255, index=True)
    patronymic = Varchar(length=255, null=True, index=True)
    birthday = Date(default=DateNow(), index=True)
    birthplace = Varchar(length=255, null=True)
    citizenship = Varchar(length=255, null=True)
    dual = Varchar(length=255, null=True)
    snils = Varchar(length=11, null=True)
    inn = Varchar(length=12, null=True, index=True)
    marital = Varchar(length=255, null=True)
    addition = Text(null=True)
    destination = Text(null=True)
    editable = Boolean(default=False)
    protected = Boolean(default=False)
    deleted = Boolean(default=False)
    user_id = ForeignKey(references=Users)
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Addresses(Table, tablename="addresses", tags=["addresses"]):
    """Table addresses."""

    id = Serial(primary_key=True, index=True)
    view = Varchar(length=255)
    address = Varchar(length=255)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Affilations(Table, tablename="affilations", tags=["affilations"]):
    """Table affilations."""

    id = Serial(primary_key=True, index=True)
    view = Varchar(length=255)
    organization = Varchar(length=255)
    inn = Varchar(length=255, null=True)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Checks(Table, tablename="checks", tags=["checks"]):
    """Table checks."""

    id = Serial(primary_key=True, index=True)
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
    conclusion = Varchar(length=255)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Contacts(Table, tablename="contacts", tags=["contacts"]):
    """Table contacts."""

    id = Serial(primary_key=True, index=True)
    view = Varchar(length=255)
    contact = Varchar(length=255)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Documents(Table, tablename="documents", tags=["documents"]):
    """Table documents."""

    id = Serial(primary_key=True, index=True)
    view = Varchar(length=255)
    series = Varchar(length=12, null=True)
    digits = Varchar(length=24)
    agency = Varchar(length=255, null=True)
    issue = Date(default=DateNow(), null=True)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Educations(Table, tablename="educations", tags=["educations"]):
    """Table educations."""

    id = Serial(primary_key=True, index=True)
    view = Varchar(length=255, null=True)
    institution = Text(null=False)
    finished = Varchar(length=4, null=True)
    specialty = Varchar(length=255, null=True)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Inquiries(Table, tablename="inquiries", tags=["inquiries"]):
    """Table inquiries."""

    id = Serial(primary_key=True, index=True)
    info = Text(null=False)
    initiator = Varchar(length=255)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Investigations(Table, tablename="investigations", tags=["investigations"]):
    """Table investigations."""

    id = Serial(primary_key=True, index=True)
    theme = Varchar(length=255)
    info = Text(null=False)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Poligrafs(Table, tablename="poligrafs", tags=["poligrafs"]):
    """Table poligrafs."""

    id = Serial(primary_key=True, index=True)
    theme = Varchar(length=255)
    results = Text(null=False)
    conclusion = Varchar(length=255)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Previous(Table, tablename="previous", tags=["previous"]):
    """Table previous."""

    id = Serial(primary_key=True, index=True)
    surname = Varchar(length=255)
    firstname = Varchar(length=255, null=True)
    patronymic = Varchar(length=255, null=True)
    changed = Varchar(length=4, null=True)
    reason = Text(null=True)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Staffs(Table, tablename="staffs", tags=["staffs"]):
    """Table staffs."""

    id = Serial(primary_key=True, index=True)
    position = Varchar(length=255)
    department = Varchar(length=255, null=True)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)


class Workplaces(Table, tablename="workplaces", tags=["workplaces"]):
    """Table workplaces."""

    id = Serial(primary_key=True, index=True)
    now_work = Boolean(default=False)
    starts = Date(default=DateNow())
    finished = Date(default=DateNow(), null=True)
    workplace = Varchar(length=255)
    address = Varchar(length=255, null=True)
    position = Varchar(length=255)
    reason = Text(null=True)
    person_id = ForeignKey(
        references=Persons,
        on_delete=OnDelete.no_action,
        on_update=OnUpdate.no_action,
        index=True,
    )
    created_at = Timestamptz(default=TimestamptzNow())
    updated_at = Timestamptz(default=TimestamptzNow(), auto_update=datetime.now)
