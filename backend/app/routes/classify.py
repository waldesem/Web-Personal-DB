from sqlalchemy import select

from . import bp
from .. import cache
from ..models.model import db, Conclusion, Role, Status, Region
from ..models.schema import (
    ConclusionSchema,
    RoleSchema,
    StatusSchema,
    RegionSchema,
)


@bp.doc(hide=True)
@cache.cached()
@bp.get("/classes")
def get_classes():
    models = [Conclusion, Role, Status, Region]
    schemas = [ConclusionSchema(), RoleSchema(), StatusSchema(), RegionSchema()]
    queries = [db.session.execute(select(model)).scalars().all() for model in models]
    results = [schema.dump(query, many=True) for query, schema in zip(queries, schemas)]
    return [{k: v for d in result for k, v in d.items()} for result in results]
