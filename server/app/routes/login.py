from datetime import datetime

import bcrypt
from flask_jwt_extended import JWTManager, current_user, \
    create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity

from . import bp
from ..models.model import TokenBlocklist, User, db
from ..models.schema import LoginSchema

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


@bp.get('/auth')
@jwt_required()
@bp.doc(hide=True)
def auth(): 
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    if user and not user.has_blocked():
        user.last_login = datetime.now()
        db.session.commit()
        return {'access': 'Authorized'}
    return {'access': 'Denied'}


@bp.post('/login')
@bp.input(LoginSchema)
@bp.doc(hide=True)
def login(response):
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()
    if user and not user.blocked:
        if bcrypt.checkpw(response['password'].encode('utf-8'), user.password):
            delta_change = datetime.now() - user.pswd_create
            if user.pswd_change and delta_change.days < 365:
                user.last_login = datetime.now()
                db.session.commit()
                access_token = create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity=user.username)
                return {'access': 'Authorized', 
                        'access_token': access_token, 
                        'refresh_token': refresh_token}
            return {"access": "Overdue", 
                    'access_token': None}
    return {"access": "Denied", 
            'access_token': None}


@bp.post("/refresh")
@bp.doc(hide=True)
@jwt_required(refresh=True)
def refresh():
    access_token = create_access_token(identity=get_jwt_identity())
    return {'access_token': access_token}
    

@bp.delete('/logout')
@bp.doc(hide=True)
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return {'access': 'Default'}


@bp.post('/password')
@bp.input(LoginSchema)
@bp.doc(hide=True)
def change_password(response):
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()
    if user:
        if bcrypt.checkpw(response['password'].encode('utf-8'), user.password):
            setattr(user, 'password', bcrypt.hashpw(response['new_pswd'].encode('utf-8'), bcrypt.gensalt()))
            setattr(user, "pswd_change", datetime.now())
            db.session.commit()
            return {"access": "Success", 
                    'access_token': None}
    return {"access": "Denied", 
            'access_token': None}
