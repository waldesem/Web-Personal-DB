from flask.views import MethodView

from . import bp
from ..models.classes import Categories, Conclusions, Roles, Groups, Statuses, Regions
from ..models.schema import models_schemas


class ClassesView(MethodView):

    @bp.doc(hide=True)
    def get(self):
        return [{i.name: i.value for i in Statuses},
                {i.name: i.value for i in Regions},
                {i.name: i.value for i in Conclusions},
                {i.name: i.value for i in Categories},
                {i.name: i.value for i in Groups},
                {i.name: i.value for i in Roles},
                {'tables': list(models_schemas.keys())}]


bp.add_url_rule('/classes', view_func=ClassesView.as_view('classes'))