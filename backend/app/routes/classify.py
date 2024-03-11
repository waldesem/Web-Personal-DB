from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .. import db, cache
from ..models.model import Conclusion, Role, Status, Region
from ..models.schema import (
    models_schemas,
    ConclusionSchema,
    RoleSchema,
    StatusSchema,
    RegionSchema,
)


class ClassesView(MethodView):
    """
    It provides methods for retrieving all the tables in the database.
    """

    @bp.doc(hide=True)
    @cache.cached()
    def get(self):
        tables = ["Conclusion", "Role", "Status", "Region"]
        queries = [
            db.session.execute(select(eval(table))).scalars().all() for table in tables
        ]
        schemas = [eval(table + "Schema")() for table in tables]
        results = [
            schema.dump(query, many=True) for query, schema in zip(queries, schemas)
        ]
        data = {table.lower(): result for table, result in zip(tables, results)}
        data["tables"] = list(models_schemas.keys())
        return data


bp.add_url_rule("/classes", view_func=ClassesView.as_view("classes"))
