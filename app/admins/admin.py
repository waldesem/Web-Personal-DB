from flask_admin import Admin
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from app.models.model import db, User, Candidate


class AdminModelView(ModelView):
    def is_accessible(self):
        return db.session.query(User.role).filter_by(username=current_user.username).first()[0] == 'admin'


admin = Admin(template_mode='bootstrap4')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(ModelView(Candidate, db.session))

