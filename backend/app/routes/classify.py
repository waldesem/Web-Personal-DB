from sqlalchemy import select

from . import bp
from .. import cache
from ..models.model import db, Conclusion, Role, Status, Region, User
from ..models.schema import (
    ConclusionSchema,
    RoleSchema,
    StatusSchema,
    RegionSchema,
    UserSchema,
)


@bp.doc(hide=True)
@cache.cached()
@bp.get("/classes")
def get_classes():
    models = [Conclusion, Role, Status, Region, User]
    schemas = [ConclusionSchema(), RoleSchema(), StatusSchema(), RegionSchema(), UserSchema()]
    queries = [db.session.execute(select(model)).scalars().all() for model in models]
    dumps = [schema.dump(query, many=True) for query, schema in zip(queries, schemas)]
    return [
        dict(
            (
                d["id"],
                d.get("conclusion")
                or d.get("role")
                or d.get("status")
                or d.get("region")
                or d.get("fullname"),
            )
            for d in sublist
        )
        for sublist in dumps
    ]
