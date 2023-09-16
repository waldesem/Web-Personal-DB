from . import bp
from ..models.classes import Category, Conclusions, Decisions, Roles, Groups, Status
from ..models.model import db, Region
    
    
@bp.get('/classify')
@bp.doc(hide=True)
def get_classes():
    """
    Get the classification data.
    This function retrieves the classification data for the API. It returns a dictionary 
    containing the values of the different status options, role options, conclusions,
    decisions, categories, groups and roles 
    """
    return [{i.name: i.value for i in Status}, 
            {rgn[0]: rgn[1] for rgn in db.session.query(Region.id, Region.region).all()}, 
            {i.name: i.value for i in Conclusions}, 
            {i.name: i.value for i in Decisions}, 
            {i.name: i.value for i in Category},
            {i.name: i.value for i in Groups},
            {i.name: i.value for i in Roles}]