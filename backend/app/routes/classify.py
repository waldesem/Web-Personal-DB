from flask.views import MethodView
from sqlalchemy import select

from . import bp
from ..models.model import async_session, \
    Category, Conclusion, Role, Group, Status, Region
from ..models.schema import models_schemas, CategorySchema, ConclusionSchema, \
    RoleSchema, GroupSchema, StatusSchema, RegionSchema


class ClassesView(MethodView):
    """The ClassesView class is a subclass of the MethodView class from the flask.views module.
    It provides methods for retrieving all the tables in the database.
    """
    decorators = [bp.doc(hide=True)]

    @bp.doc(hide=True)
    async def get(self):
        async with async_session() as session:
            data = {}
            tables = ['Category', 'Conclusion', 'Role', 'Group', 'Status', 'Region']
            for table in tables:
                result = await session.execute(select(eval(table)).all())
                schema = eval(table + 'Schema')(many=True)
                data[table.lower()] = schema.dump(result)
            data['tables'] = list(models_schemas.keys())
            return data
        
bp.add_url_rule('/classes', view_func=ClassesView.as_view('classes'))