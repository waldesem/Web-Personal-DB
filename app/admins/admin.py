from flask_admin import Admin
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from app.models.model import db, User, Candidate, Staff, Document, Address, Contact, Workplace, RelationShip, \
    Check, Registry, Poligraf, Investigation, Inquiry


class AdminModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated)


admin = Admin()
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Candidate, db.session))
admin.add_view(ModelView(Staff, db.session))
admin.add_view(ModelView(Document, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(Workplace, db.session))
admin.add_view(ModelView(RelationShip, db.session))
admin.add_view(ModelView(Check, db.session))
admin.add_view(ModelView(Registry, db.session))
admin.add_view(ModelView(Poligraf, db.session))
admin.add_view(ModelView(Investigation, db.session))
admin.add_view(ModelView(Inquiry, db.session))
