from flask.views import MethodView

from . import bp
from ..models.classes import Category, Conclusions, \
    Decisions, Roles, Groups, Status, Regions
from ..models.schema import models_schemas


class ClassesView(MethodView):

    @bp.doc(hide=True)
    def get(self):
        return [{i.name: i.value for i in Status},
                {index: i.value for index, i in enumerate(Regions, 1)},
                {i.name: i.value for i in Conclusions},
                {i.name: i.value for i in Decisions},
                {i.name: i.value for i in Category},
                {i.name: i.value for i in Groups},
                {i.name: i.value for i in Roles},
                models_schemas.keys()]


bp.add_url_rule('/classes', view_func=ClassesView.as_view('classes'))
