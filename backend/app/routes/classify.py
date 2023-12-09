from flask.views import MethodView

from . import bp
from .. import db
from ..models.model import Category, Conclusion, Role, Group, Status, Region
from ..models.schema import models_schemas, CategorySchema, ConclusionSchema, \
    RoleSchema, GroupSchema, StatusSchema, RegionSchema


class ClassesView(MethodView):
    """
    It provides methods for retrieving all the tables in the database.
    """

    @bp.doc(hide=True)
    def get(self):
        data = {}
        tables = ['Category', 'Conclusion', 'Role', 'Group', 'Status', 'Region']
        for table in tables:
            result = db.session.query(eval(table)).all()
            schema = eval(table + 'Schema')(many=True)
            data[table.lower()] = schema.dump(result.scalars())
        data['tables'] = list(models_schemas.keys())
        return data
        
bp.add_url_rule('/classes', view_func=ClassesView.as_view('classes'))