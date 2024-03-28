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
    tables = ["Conclusion", "Role", "Status", "Region"]
    queries = [
        db.session.execute(select(eval(table))).scalars().all() for table in tables
    ]
    schemas = [eval(table + "Schema")() for table in tables]
    results = [
        schema.dump(query, many=True) for query, schema in zip(queries, schemas)
    ]
    data = {table.lower(): result for table, result in zip(tables, results)}
    return data
