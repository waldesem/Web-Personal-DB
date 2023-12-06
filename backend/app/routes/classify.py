# from flask.views import MethodView
# from sqlalchemy import select

# from . import bp
# from ..models.model import async_session, \
#     Category, Conclusion, Role, Group, Status, Region
# from ..models.schema import models_schemas, CategorySchema, ConclusionSchema, \
#     RoleSchema, GroupSchema, StatusSchema, RegionSchema


# class ClassesView(MethodView):
#     """
#     It provides methods for retrieving all the tables in the database.
#     """

#     @bp.doc(hide=True)
#     async def get(self):
#         async with async_session() as session:
#             data = {}
#             tables = ['Category', 'Conclusion', 'Role', 'Group', 'Status', 'Region']
#             for table in tables:
#                 result = await session.execute(select(eval(table)))
#                 schema = eval(table + 'Schema')(many=True)
#                 data[table.lower()] = schema.dump(result.all())
#             data['tables'] = list(models_schemas.keys())
#             return data
        
# bp.add_url_rule('/classes', view_func=ClassesView.as_view('classes'))