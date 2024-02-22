from apiflask import EmptySchema
from flask import abort
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .. import db
from .login import roles_required, group_required
from ..models.classes import Roles, Groups
from ..models.model import (
    Staff,
    Document,
    Address,
    Contact,
    Workplace,
    Relation,
    Affilation,
)
from ..models.schema import (
    RelationSchema,
    StaffSchema,
    AddressSchema,
    ContactSchema,
    DocumentSchema,
    WorkplaceSchema,
    AffilationSchema,
)


class StaffView(MethodView):

    decorators = [group_required(Groups.staffsec.value), bp.doc(hide=True)]

    def get(self, item_id):
        return (
            StaffSchema().dump(
                db.session.execute(
                    select(Staff).filter_by(person_id=item_id).order_by(Staff.id.desc())
                )
                .scalars()
                .all(),
                many=True,
            ),
            200,
        )

    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    def post(self, item_id, json_data):
        db.session.add(Staff(**json_data | {"person_id": item_id}))
        db.session.commit()
        return "", 201

    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    def patch(self, item_id, json_data):
        staff = db.session.get(Staff, item_id)
        if staff:
            for k, v in json_data.items():
                setattr(staff, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        staff = db.session.get(Staff, item_id)
        if staff:
            db.session.delete(staff)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule("/staff/<int:item_id>", view_func=StaffView.as_view("staff"))


class DocumentView(MethodView):

    decorators = [group_required(Groups.staffsec.value), bp.doc(hide=True)]

    def get(self, item_id):
        return (
            DocumentSchema().dump(
                db.session.execute(
                    select(Document)
                    .filter_by(person_id=item_id)
                    .order_by(Document.id.desc())
                )
                .scalars()
                .all(),
                many=True,
            ),
            200,
        )

    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    def post(self, item_id, json_data):
        db.session.add(Document(**json_data | {"person_id": item_id}))
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    def patch(self, item_id, json_data):
        docum = db.session.get(Document, item_id)
        if docum:
            for k, v in json_data.items():
                setattr(docum, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, item_id):
        docum = db.session.get(Document, item_id)
        if docum:
            db.session.delete(docum)
            db.session.commit()
            return ""
        return abort(403)


bp.add_url_rule(
    "/document/<int:item_id>", view_func=DocumentView.as_view("document")
)


class AddressView(MethodView):

    decorators = [group_required(Groups.staffsec.value), bp.doc(hide=True)]

    def get(self, item_id):
        return (
            AddressSchema().dump(
                db.session.execute(
                    select(Address)
                    .filter_by(person_id=item_id)
                    .order_by(Address.id.desc())
                )
                .scalars()
                .all(),
                many=True,
            ),
            200,
        )

    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    def post(self, item_id, json_data):
        db.session.add(Address(**json_data | {"person_id": item_id}))
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    def patch(self, item_id, json_data):
        addr = db.session.get(Address, item_id)
        if addr:
            for k, v in json_data.items():
                setattr(addr, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        addr = db.session.get(Address, item_id)
        if addr:
            db.session.delete(addr)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule(
    "/address/<int:item_id>", view_func=AddressView.as_view("address")
)


class ContactView(MethodView):

    decorators = [group_required(Groups.staffsec.value), bp.doc(hide=True)]

    def get(self, item_id):
        return ContactSchema().dump(
            db.session.execute(
                select(Contact).filter_by(person_id=item_id).order_by(Contact.id.desc())
            )
            .scalars()
            .all(),
            many=True,
        )

    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    def post(self, item_id, json_data):
        db.session.add(Contact(**json_data | {"person_id": item_id}))
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    def patch(self, item_id, json_data):
        cont = db.session.get(Contact, item_id)
        if cont:
            for k, v in json_data.items():
                setattr(cont, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        cont = db.session.get(Contact, item_id)
        if cont:
            db.session.delete(cont)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule(
    "/contact/<int:item_id>", view_func=ContactView.as_view("contact")
)


class WorkplaceView(MethodView):

    decorators = [group_required(Groups.staffsec.value), bp.doc(hide=True)]

    def get(self, item_id):
        return (
            WorkplaceSchema().dump(
                db.session.execute(
                    select(Workplace)
                    .filter_by(person_id=item_id)
                    .order_by(Workplace.id.desc())
                )
                .scalars()
                .all(),
                many=True,
            ),
            200,
        )

    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def post(self, item_id, json_data):
        json_data["now_work"] = (
            bool(json_data.pop("now_work")) if "now_work" in json_data else False
        )
        db.session.add(Workplace(**json_data | {"person_id": item_id}))
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def patch(self, item_id, json_data):
        json_data["now_work"] = (
            bool(json_data.pop("now_work")) if "now_work" in json_data else False
        )
        work = db.session.get(Workplace, item_id)
        if work:
            for k, v in json_data.items():
                setattr(work, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        work = db.session.get(Workplace, item_id)
        if work:
            db.session.delete(work)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule(
    "/workplace/<int:item_id>", view_func=WorkplaceView.as_view("workplace")
)


class RelationView(MethodView):

    decorators = [group_required(Groups.staffsec.value), bp.doc(hide=True)]

    def get(self, item_id):
        return (
            RelationSchema().dump(
                db.session.execute(
                    select(Relation)
                    .filter_by(person_id=item_id)
                    .order_by(Relation.id.desc())
                )
                .scalars()
                .all(),
                many=True,
            ),
            200,
        )

    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    def post(self, item_id, json_data):
        db.session.add(Relation(**json_data | {"person_id": item_id}))
        db.session.add(
            Relation(
                relation=json_data["relation"],
                relation_id=item_id,
                person_id=json_data["relation_id"],
            )
        )
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    def patch(self, item_id, json_data):
        rel = db.session.get(Relation, item_id)
        if rel:
            for k, v in json_data.items():
                setattr(rel, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        rel = db.session.get(Relation, item_id)
        if rel:
            db.session.delete(rel)
            db.session.commit()
            return ""
        return abort(403)


bp.add_url_rule(
    "/relation/<int:item_id>", view_func=RelationView.as_view("relation")
)


class AffilationView(MethodView):

    decorators = [group_required(Groups.staffsec.value), bp.doc(hide=True)]

    def get(self, item_id):
        return AffilationSchema().dump(
            db.session.execute(
                select(Affilation)
                .filter_by(person_id=item_id)
                .order_by(Affilation.id.desc())
            )
            .scalars()
            .all(),
            many=True,
        )

    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    def post(self, item_id, json_data):
        db.session.add(Affilation(**json_data | {"person_id": item_id}))
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    def patch(self, item_id, json_data):
        affil = db.session.get(Affilation, item_id)
        if affil:
            for k, v in json_data.items():
                setattr(affil, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        affil = db.session.get(Affilation, item_id)
        if affil:
            db.session.delete(affil)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule(
    "/affilation/<int:item_id>", view_func=AffilationView.as_view("affilation")
)
