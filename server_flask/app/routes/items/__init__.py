from flask import Blueprint

from .addresses import bp as addresses_bp
from .affilations import bp as affilations_bp
from .checks import bp as checks_bp
from .contacts import bp as contacts_bp
from .documents import bp as documents_bp
from .educations import bp as educations_bp
from .inquiries import bp as inquiries_bp
from .investigations import bp as investigations_bp
from .persons import bp as persons_bp
from .poligrafs import bp as poligrafs_bp
from .previous import bp as previous_bp
from .relations import bp as relations_bp
from .staffs import bp as staffs_bp
from .workplaces import bp as workplaces_bp

bp = Blueprint("items", __name__, url_prefix="/items")

bp.register_blueprint(addresses_bp)
bp.register_blueprint(affilations_bp)
bp.register_blueprint(checks_bp)
bp.register_blueprint(contacts_bp)
bp.register_blueprint(documents_bp)
bp.register_blueprint(educations_bp)
bp.register_blueprint(inquiries_bp)
bp.register_blueprint(investigations_bp)
bp.register_blueprint(persons_bp)
bp.register_blueprint(poligrafs_bp)
bp.register_blueprint(previous_bp)
bp.register_blueprint(relations_bp)
bp.register_blueprint(staffs_bp)
bp.register_blueprint(workplaces_bp)
