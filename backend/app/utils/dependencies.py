import uuid
from datetime import datetime, timezone
from functools import wraps

from flask import abort, request
import jwt
from jwt.exceptions import InvalidTokenError as JWTError
from sqlalchemy.orm import Session
from sqlalchemy import select

from config import Config
from ..models.model import engine, TokenBlocklist, User


class Token:

    current_user = None
    decoded_token = None
    
    @classmethod 
    def get_auth(cls, token):
        Token.current_user = None 
        Token.decoded_token = None
        try:
            token = token.replace("Bearer ", "")  # Remove "Bearer " prefix
            decoded = jwt.decode(
                token, 
                Config.JWT_SECRET_KEY, 
                algorithms=[Config.jwt_tokens_algorithm]
            )
            with Session(engine) as session:
                result = session.execute(
                    select(TokenBlocklist)
                    .filter_by(jti=decoded["jti"])
                ).all()
                if not result:
                    user_id = decoded.get("sub")
                    if user_id:
                        user = session.get(User, user_id)
                        if user: 
                            Token.current_user = user
                            Token.decoded_token = decoded
                            return True
                return False 
        except JWTError as e:
            print(e)
            return False 


def create_token(cridentials, token_type):
    data = {"sub": cridentials, "type": token_type, "jti": str(uuid.uuid4())}
    if token_type == "access":
        data["exp"] = datetime.now(timezone.utc) + Config.JWT_ACCESS_TOKEN_EXPIRES
    else:
        data["exp"] = datetime.now(timezone.utc) + Config.JWT_REFRESH_TOKEN_EXPIRES
    return jwt.encode(
        data, Config.JWT_SECRET_KEY, algorithm=Config.jwt_tokens_algorithm
    )


def jwt_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if Token.get_auth(header):
                return func(*args, **kwargs)
            else:
                abort(404)
        return wrapper
    return decorator

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if Token.get_auth(header):
                if any(r.role in roles for r in Token.current_user.roles):
                    return func(*args, **kwargs)
                else:
                    abort(404)
            else:
                abort(404)
        return wrapper
    return decorator
