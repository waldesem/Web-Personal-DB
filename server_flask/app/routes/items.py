"""Items routes."""

from typing import Literal

from flask import Blueprint, current_app
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.validate import serialize, validate
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


def get_item(item: Items, item_id: int) -> list[DeclarativeBase]:
    """Retrieve an item from the database based on the provided item."""
    stmt = (
        db.metatables[item]
        .select()
        .filter(db.metatables[item].c.person_id == item_id)
        .order_by(db.metatables[item].c.id.desc())
    )
    return db.session.execute(stmt).all()


def post_item(item: Items, item_id: int, json_data: BaseModel) -> str:
    """Insert or replaces a record in the specified table with the given item ID."""
    try:
        json_dict = json_data.dict(exclude_none=True, exclude={"created"})
        json_dict["person_id"] = item_id
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
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return {"message": "error"}, 500
    else:
        return {"message": "success"}, 200


@bp.get("/previous/<int:item_id>")
@serialize(Prev, orm=True, many=True)
@validate
@auth_required()
def get_previous(item_id: int) -> tuple[list[Previous], int]:
    """Retrieve a list of previous names from the database."""
    return get_item("previous", item_id), 200


@bp.get("/educations/<int:item_id>")
@serialize(Education, orm=True, many=True)
@validate
@auth_required()
def get_educations(item_id: int) -> tuple[list[Educations], int]:
    """Retrieve a list of educations from the database."""
    return get_item("educations", item_id), 200


@bp.get("/addresses/<int:item_id>")
@serialize(Address, orm=True, many=True)
@validate
@auth_required()
def get_addresses(item_id: int) -> tuple[list[Addresses], int]:
    """Retrieve a list of addresses from the database."""
    return get_item("addresses", item_id), 200


@bp.get("/affilations/<int:item_id>")
@serialize(Affilation, orm=True, many=True)
@validate
@auth_required()
def get_affilations(item_id: int) -> tuple[list[Affilations], int]:
    """Retrieve a list of affilations from the database."""
    return get_item("affilations", item_id), 200


@bp.get("/staffs/<int:item_id>")
@serialize(Staff, orm=True, many=True)
@validate
@auth_required()
def get_staffs(item_id: int) -> tuple[list[Staffs], int]:
    """Retrieve a list of staffs from the database."""
    return get_item("staffs", item_id), 200


@bp.get("/workplaces/<int:item_id>")
@serialize(Workplace, orm=True, many=True)
@validate
@auth_required()
def get_workplaces(item_id: int) -> tuple[list[Workplaces], int]:
    """Retrieve a list of workplaces from the database."""
    return get_item("workplaces", item_id), 200


@bp.get("/contacts/<int:item_id>")
@serialize(Contact, orm=True, many=True)
@validate
@auth_required()
def get_contacts(item_id: int) -> tuple[list[Contacts], int]:
    """Retrieve a list of contacts from the database."""
    return get_item("contacts", item_id), 200


@bp.get("/documents/<int:item_id>")
@serialize(Document, orm=True, many=True)
@validate
@auth_required()
def get_documents(item_id: int) -> tuple[list[Documents], int]:
    """Retrieve a list of documents from the database."""
    return get_item("documents", item_id), 200


@bp.get("/checks/<int:item_id>")
@serialize(Check, orm=True, many=True)
@validate
@auth_required()
def get_checks(item_id: int) -> tuple[list[Checks], int]:
    """Retrieve a list of checks from the database."""
    return get_item("checks", item_id), 200


@bp.get("/poligrafs/<int:item_id>")
@serialize(Poligraf, orm=True, many=True)
@validate
@auth_required()
def get_poligrafs(item_id: int) -> tuple[list[Poligrafs], int]:
    """Retrieve a list of poligrafs from the database."""
    return get_item("poligrafs", item_id), 200


@bp.get("/inquiries/<int:item_id>")
@serialize(Inquiry, orm=True, many=True)
@validate
@auth_required()
def get_inquiries(item_id: int) -> tuple[list[Inquiries], int]:
    """Retrieve a list of inquiries from the database."""
    return get_item("inquiries", item_id), 200


@bp.get("/investigations/<int:item_id>")
@serialize(Investigation, orm=True, many=True)
@validate
@auth_required()
def get_investigations(item_id: int) -> tuple[list[Investigations], int]:
    """Retrieve a list of investigations from the database."""
    return get_item("investigations", item_id), 200


@bp.post("/previous/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_previous(item_id: int, json_data: Prev) -> tuple[str, int]:
    """Insert or replaces a record in previous table with the given item ID."""
    return post_item("previous", item_id, json_data)


@bp.post("/educations/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_educations(item_id: int, json_data: Education) -> tuple[str, int]:
    """Insert or replaces a record in educations table with the given item ID."""
    return post_item("educations", item_id, json_data)


@bp.post("/addresses/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_addresses(item_id: int, json_data: Address) -> tuple[str, int]:
    """Insert or replaces a record in addresses table with the given item ID."""
    return post_item("addresses", item_id, json_data)


@bp.post("/affilations/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_affilations(item_id: int, json_data: Affilation) -> tuple[str, int]:
    """Insert or replaces a record in affilations table with the given item ID."""
    return post_item("affilations", item_id, json_data)


@bp.post("/staffs/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_staffs(item_id: int, json_data: Staff) -> tuple[str, int]:
    """Insert or replaces a record in staffs table with the given item ID."""
    return post_item("staffs", item_id, json_data)


@bp.post("/workplaces/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_workplaces(item_id: int, json_data: Workplace) -> tuple[str, int]:
    """Insert or replaces a record in workplaces table with the given item ID."""
    return post_item("workplaces", item_id, json_data)


@bp.post("/contacts/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_contacts(item_id: int, json_data: Contact) -> tuple[str, int]:
    """Insert or replaces a record in contacts table with the given item ID."""
    return post_item("contacts", item_id, json_data)


@bp.post("/documents/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_documents(item_id: int, json_data: Document) -> tuple[str, int]:
    """Insert or replaces a record in documents table with the given item ID."""
    return post_item("documents", item_id, json_data)


@bp.post("/checks/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_checks(item_id: int, json_data: Check) -> tuple[str, int]:
    """Insert or replaces a record in checks table with the given item ID."""
    return post_item("checks", item_id, json_data)


@bp.post("/poligrafs/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_poligrafs(item_id: int, json_data: Poligraf) -> tuple[str, int]:
    """Insert or replaces a record in poligrafs table with the given item ID."""
    return post_item("poligrafs", item_id, json_data)


@bp.post("/inquiries/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_inquiries(item_id: int, json_data: Inquiry) -> tuple[str, int]:
    """Insert or replaces a record in inquiries table with the given item ID."""
    return post_item("inquiries", item_id, json_data)


@bp.post("/investigations/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def post_investigations(item_id: int, json_data: Investigation) -> tuple[str, int]:
    """Insert or replaces a record in investigations table with the given item ID."""
    return post_item("investigations", item_id, json_data)


@bp.delete("/<item>/<int:item_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def delete(item: Items, item_id: int) -> tuple[str, int]:
    """Delete an item from the database based on the provided item name and item ID."""
    try:
        db.session.execute(
            db.metatables[item].delete().where(db.metatables[item].c.id == item_id),
        )
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return {"message": "error"}, 500
    else:
        return {"message": "success"}, 201
