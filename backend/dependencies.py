from datetime import datetime, timezone
from typing import Annotated
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from jose import JWTError, jwt

from .config import Settings
from .models.model import engine, TokenBlocklist, User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
    

def create_token(cridentials: str, token_type: str):
    data = {"sub": cridentials, "type": cridentials, "jti": str(uuid.uuid4())}
    if token_type == "access":
        data["exp"] = datetime.now(timezone.utc) + Settings.jwt_access_token_expires
    if token_type == "refresh":
        data["exp"] = datetime.now(timezone.utc) + Settings.jwt_refresh_token_expires
    return jwt.encode(
        data, Settings.jwt_secret_key, algorithm=Settings.jwt_tokens_algorithm
    )


def jwt_required(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        decoded = jwt.decode(
            token, Settings.jwt_secret_key, algorithms=[Settings.jwt_tokens_algorithm]
        )
        return decoded
    except JWTError:
        raise credentials_exception


def get_jwt_blocklist(token: Annotated[str, Depends(jwt_required)]):
    with Session(engine) as session:
        result = session.exec(
            select(TokenBlocklist).filter_by(jti=token["jti"])
        ).all()
        if not result:
            return token
        else:
            raise credentials_exception


def login_required(token: Annotated[str, Depends(get_jwt_blocklist)]):
    user_id: str = token.get("sub")
    if user_id is None:
        raise credentials_exception
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise credentials_exception
    return user


class Permission:

    def __init__(self, roles: list[str]) -> None:
        self.roles = roles

    def __call__(self, user: User = Depends(login_required)) -> bool:
        if not any(r.role in self.roles for r in user.roles):
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Permissions'
                )
        return user