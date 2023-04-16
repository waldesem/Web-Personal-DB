from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models.model import db, User

admin = Admin()
admin.add_view(ModelView(User, db.session))
