"""Items routes."""

from typing import Literal

from flask import Blueprint, current_app
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from app import caching, db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.validize import pydantify
from app.models.models import (
    Address,
    Affilation,
    Check,
    Contact,
    Document,
    Education,
    Inquiry,
    Investigation,
    Poligraf,
    Prev,
    Staff,
    Workplace,
)
from app.tables.tables import (
    Addresses,
    Affilations,
    Checks,
    Contacts,
    Documents,
    Educations,
    Inquiries,
    Investigations,
    Poligrafs,
    Previous,
    Staffs,
    Workplaces,
)

bp = Blueprint("items", __name__)

Items = Literal[
    "addresses",
    "affilations",
    "checks",
    "contacts",
    "documents",
    "educations",
    "inquiries",
    "investigations",
    "previous",
    "poligrafs",
    "staffs",
    "workplaces",
]


def get_item(item: Items, person_id: int) -> list[DeclarativeBase]:
    """Retrieve an item from the database based on the provided item."""
    if cached_data := caching.get_data(person_id, item):
        return cached_data
    stmt = (
        db.metatables[item]
        .select()
        .filter(db.metatables[item].c.person_id == person_id)
        .order_by(db.metatables[item].c.id.desc())
    )
    result = db.session.execute(stmt).all()
    caching.set_data(person_id, result, item)
    return result


def post_item(item: Items, person_id: int, json_data: BaseModel) -> str:
    """Insert or replaces a record in the specified table with the given item ID."""
    try:
        json_dict = json_data.dict(exclude_none=True, exclude={"created"})
        json_dict["person_id"] = person_id
        # Проверяем, есть ли ключ "id" в словаре json_dict
        if item_id := json_dict.pop("id", None):
            # Если есть, создаем запрос на обновление записи с указанным id
            stmt = (
                db.metatables[item]
                .update()
                .where(db.metatables[item].c.id == item_id)
                .values(json_dict)
            )
        else:
            # Если нет, создаем запрос на вставку новой записи
            stmt = db.metatables[item].insert().values(json_dict)
        db.session.execute(stmt)
        db.session.commit()
        # Удаление устаревших данных из кэша
        caching.set_data(person_id, [], item)
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return {"message": "error"}, 400
    else:
        return {"message": "success"}, 200


@bp.get("/previous/<int:person_id>")
@pydantify(Prev, orm=True, many=True)
@auth_required()
def get_previous(person_id: int) -> tuple[list[Previous], int]:
    """Retrieve a list of previous names from the database."""
    return get_item("previous", person_id), 200


@bp.get("/educations/<int:person_id>")
@pydantify(Education, orm=True, many=True)
@auth_required()
def get_educations(person_id: int) -> tuple[list[Educations], int]:
    """Retrieve a list of educations from the database."""
    return get_item("educations", person_id), 200


@bp.get("/addresses/<int:person_id>")
@pydantify(Address, orm=True, many=True)
@auth_required()
def get_addresses(person_id: int) -> tuple[list[Addresses], int]:
    """Retrieve a list of addresses from the database."""
    return get_item("addresses", person_id), 200


@bp.get("/affilations/<int:person_id>")
@pydantify(Affilation, orm=True, many=True)
@auth_required()
def get_affilations(person_id: int) -> tuple[list[Affilations], int]:
    """Retrieve a list of affilations from the database."""
    return get_item("affilations", person_id), 200


@bp.get("/staffs/<int:person_id>")
@pydantify(Staff, orm=True, many=True)
@auth_required()
def get_staffs(person_id: int) -> tuple[list[Staffs], int]:
    """Retrieve a list of staffs from the database."""
    return get_item("staffs", person_id), 200


@bp.get("/workplaces/<int:person_id>")
@pydantify(Workplace, orm=True, many=True)
@auth_required()
def get_workplaces(person_id: int) -> tuple[list[Workplaces], int]:
    """Retrieve a list of workplaces from the database."""
    return get_item("workplaces", person_id), 200


@bp.get("/contacts/<int:person_id>")
@pydantify(Contact, orm=True, many=True)
@auth_required()
def get_contacts(person_id: int) -> tuple[list[Contacts], int]:
    """Retrieve a list of contacts from the database."""
    return get_item("contacts", person_id), 200


@bp.get("/documents/<int:person_id>")
@pydantify(Document, orm=True, many=True)
@auth_required()
def get_documents(person_id: int) -> tuple[list[Documents], int]:
    """Retrieve a list of documents from the database."""
    return get_item("documents", person_id), 200


@bp.get("/checks/<int:person_id>")
@pydantify(Check, orm=True, many=True)
@auth_required()
def get_checks(person_id: int) -> tuple[list[Checks], int]:
    """Retrieve a list of checks from the database."""
    return get_item("checks", person_id), 200


@bp.get("/poligrafs/<int:person_id>")
@pydantify(Poligraf, orm=True, many=True)
@auth_required()
def get_poligrafs(person_id: int) -> tuple[list[Poligrafs], int]:
    """Retrieve a list of poligrafs from the database."""
    return get_item("poligrafs", person_id), 200


@bp.get("/inquiries/<int:person_id>")
@pydantify(Inquiry, orm=True, many=True)
@auth_required()
def get_inquiries(person_id: int) -> tuple[list[Inquiries], int]:
    """Retrieve a list of inquiries from the database."""
    return get_item("inquiries", person_id), 200


@bp.get("/investigations/<int:person_id>")
@pydantify(Investigation, orm=True, many=True)
@auth_required()
def get_investigations(person_id: int) -> tuple[list[Investigations], int]:
    """Retrieve a list of investigations from the database."""
    return get_item("investigations", person_id), 200


@bp.post("/previous/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_previous(person_id: int, json_data: Prev) -> tuple[str, int]:
    """Insert or replaces a record in previous table with the given item ID."""
    return post_item("previous", person_id, json_data)


@bp.post("/educations/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_educations(person_id: int, json_data: Education) -> tuple[str, int]:
    """Insert or replaces a record in educations table with the given item ID."""
    return post_item("educations", person_id, json_data)


@bp.post("/addresses/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_addresses(person_id: int, json_data: Address) -> tuple[str, int]:
    """Insert or replaces a record in addresses table with the given item ID."""
    return post_item("addresses", person_id, json_data)


@bp.post("/affilations/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_affilations(person_id: int, json_data: Affilation) -> tuple[str, int]:
    """Insert or replaces a record in affilations table with the given item ID."""
    return post_item("affilations", person_id, json_data)


@bp.post("/staffs/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_staffs(person_id: int, json_data: Staff) -> tuple[str, int]:
    """Insert or replaces a record in staffs table with the given item ID."""
    return post_item("staffs", person_id, json_data)


@bp.post("/workplaces/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_workplaces(person_id: int, json_data: Workplace) -> tuple[str, int]:
    """Insert or replaces a record in workplaces table with the given item ID."""
    return post_item("workplaces", person_id, json_data)


@bp.post("/contacts/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_contacts(person_id: int, json_data: Contact) -> tuple[str, int]:
    """Insert or replaces a record in contacts table with the given item ID."""
    return post_item("contacts", person_id, json_data)


@bp.post("/documents/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_documents(person_id: int, json_data: Document) -> tuple[str, int]:
    """Insert or replaces a record in documents table with the given item ID."""
    return post_item("documents", person_id, json_data)


@bp.post("/checks/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_checks(person_id: int, json_data: Check) -> tuple[str, int]:
    """Insert or replaces a record in checks table with the given item ID."""
    return post_item("checks", person_id, json_data)


@bp.post("/poligrafs/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_poligrafs(person_id: int, json_data: Poligraf) -> tuple[str, int]:
    """Insert or replaces a record in poligrafs table with the given item ID."""
    return post_item("poligrafs", person_id, json_data)


@bp.post("/inquiries/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_inquiries(person_id: int, json_data: Inquiry) -> tuple[str, int]:
    """Insert or replaces a record in inquiries table with the given item ID."""
    return post_item("inquiries", person_id, json_data)


@bp.post("/investigations/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_investigations(person_id: int, json_data: Investigation) -> tuple[str, int]:
    """Insert or replaces a record in investigations table with the given item ID."""
    return post_item("investigations", person_id, json_data)


@bp.delete("/<item>/<int:item_id>/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def delete(item: Items, item_id: int, person_id: int) -> tuple[str, int]:
    """Delete an item from the database based on the provided item name and item ID."""
    try:
        db.session.execute(
            db.metatables[item].delete().where(db.metatables[item].c.id == item_id),
        )
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return {"message": "error"}, 400
    else:
        caching.set_data(str(person_id), item, [])
        return {"message": "success"}, 201
