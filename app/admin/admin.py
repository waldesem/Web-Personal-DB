from flask_admin import Admin
from flask import abort
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from app.models.model import db, User, Role, Candidate


admin = Admin(template_mode='bootstrap4')


class AdminModelView(ModelView):

    def is_accessible(self):
        if current_user.has_role('admin'):
            return True
        else:
            abort(403)


admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(AdminModelView(Candidate, db.session))
admin.add_link(MenuLink(name='Return', url='/'))
