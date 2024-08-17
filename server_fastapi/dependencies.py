import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError as JWTError
from sqlmodel import Session, select

from .config import settings
from .models.model import TokenBlocklist, User, engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_token(cridentials: str, token_type: str):
    """
    Generates a JSON Web Token (JWT) based on the provided credentials and token type.

    Args:
        cridentials (str): The credentials to be included in the token.
        token_type (str): The type of token to be generated. Must be either "access" or "refresh".

    Returns:
        str: The generated JWT.

    Raises:
        None.

    Notes:
        - The generated token includes the following claims: "sub", "type", and "jti".
        - The "sub" claim is set to the provided credentials.
        - The "type" claim is also set to the provided credentials.
        - The "jti" claim is set to a randomly generated UUID.
        - The token expiration is determined based on the token type:
            - For "access" tokens, the expiration is set to the current UTC datetime plus the value of `settings.jwt_access_token_expires`.
            - For "refresh" tokens, the expiration is set to the current UTC datetime plus the value of `settings.jwt_refresh_token_expires`.
        - The token is encoded using the `jwt.encode` function from the `jwt` module, with the `settings.jwt_secret_key` as the secret key and `settings.jwt_tokens_algorithm` as the algorithm.
    """
    data = {"sub": cridentials, "type": cridentials, "jti": str(uuid.uuid4())}
    if token_type == "access":
        data["exp"] = datetime.now(timezone.utc) + settings.jwt_access_token_expires
    else:
        data["exp"] = datetime.now(timezone.utc) + settings.jwt_refresh_token_expires
    return jwt.encode(
        data, settings.jwt_secret_key, algorithm=settings.jwt_tokens_algorithm
    )


def jwt_required(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Decorator function that checks if a JWT token is valid.

    Args:
        token (Annotated[str, Depends(oauth2_scheme)]): The JWT token to be decoded.

    Returns:
        dict: The decoded JWT token.

    Raises:
        credentials_exception: If the token is invalid or cannot be decoded.
    """
    try:
        decoded = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_tokens_algorithm]
        )
        return decoded
    except JWTError:
        raise credentials_exception


def get_jwt_blocklist(token: Annotated[str, Depends(jwt_required)]):
    """
    Retrieves a JWT token from the blocklist.

    Args:
        token (Annotated[str, Depends(jwt_required)]): The JWT token to be checked against the blocklist.

    Returns:
        str: The JWT token if it is not found in the blocklist.

    Raises:
        credentials_exception: If the token is found in the blocklist.
    """
    with Session(engine) as session:
        result = session.exec(select(TokenBlocklist).filter_by(jti=token["jti"])).all()
        if not result:
            return token
        raise credentials_exception


def login_required(token: Annotated[str, Depends(get_jwt_blocklist)]):
    """
    Decorator function that checks if a JWT token is valid and retrieves the corresponding user.

    Args:
        token (Annotated[str, Depends(get_jwt_blocklist)]): The JWT token to be checked against the blocklist.

    Returns:
        User

    Raises:
        credentials_exception: If the token is invalid or cannot be decoded.
    """
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
        """
        Initializes the Permission object with the given roles.

        Args:
            roles (list[str]): A list of strings representing the roles assigned to the user.

        Returns:
            None
        """
        self.roles = roles

    def __call__(self, user: User = Depends(login_required)) -> bool:
        if not any(r.role in self.roles for r in user.roles):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Permissions"
            )
        return user
