from datetime import datetime, timezone
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ldap3 import Server, Connection, ALL

from ..models.schema import LoginSchema, TokenSchema
from ..models.model import engine, User, TokenBlocklist
from ..utils.token import jwt_required, login_required, create_token


auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.get("/", status_code=200)
async def get_auth(current_user: Annotated[User, Depends(login_required)]) -> User:
    """
    Retrieves the current authenticated user from the database.
    """
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == current_user.username)
        ).one_or_none()
        if user and not user.blocked and not user.deleted:
            user.last_login = datetime.now()
            session.commit()
            return user



@auth.post("/login", status_code=201)
async def post_login(json_data: LoginSchema) -> TokenSchema:
    """
    Post method for the given API endpoint.
    """
    # ldap = ldap_auth(json_data["username"], json_data["password"])
    # if ldap:
    #     user = User.get_user(json_data["username"])
    #     if not user:
    #         user = User(
    #         fullname=ldap["fullname"],
    #         email=ldap["email"],
    #         username=json_data["username"],
    #         )
    #     )
    #         db.session.add(user)
    #         db.session.flush()
    #         user.roles.append(
    #             db.session.execute(
    #                 select(Role).filter_by(role=(Roles.user.value))
    #                 ).scalar_one_or_none()
    #         )
    #     if not user.deleted and not user.blocked:
    #         user.last_login = datetime.now()
    #         token = UserSchema().dump(user)
    #         db.session.commit()
    #         return {
    #             "message": "Authenticated",
    #             "access_token": create_access_token(identity=token),
    #             "refresh_token": create_refresh_token(identity=token),
    #         }, 201

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == json_data.username)
        ).one_or_none()
        if user and not user.blocked and not user.deleted:
            if bcrypt.checkpw(json_data.password.encode("utf-8"), user.password):
                delta_change = datetime.now(timezone.utc) - user.pswd_created
                if not user.change_pswd and delta_change.days < 365:
                    user.last_login = datetime.now(timezone.utc)
                    user.attempt = 0
                    session.commit()
                    return {
                        "message": "Authenticated",
                        "access_token": create_token(str(user.id), "access"),
                        "refresh_token": create_token(str(user.id), "refresh"),
                    }
                return {"message": "Overdue"}
            else:
                if user.attempt < 9:
                    user.attempt += 1
                else:
                    user.blocked = True
                session.commit()

        return {"message": "Denied"}


@auth.patch("/login", status_code=201)
async def patch_password(json_data: LoginSchema):
    """
    Patch method for updating user password.
    """
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == json_data.username)
        ).one_or_none()
        if (
            user
            and not user.blocked
            and bcrypt.checkpw(json_data.password.encode("utf-8"), user.password)
        ):
            user.password = bcrypt.hashpw(json_data.new_pswd.encode("utf-8"), bcrypt.gensalt())
            user.change_pswd = False
            session.commit()
            return {"message": "Changed"}
        return {"message": "Denied"}


@auth.delete("/login", status_code=204)
async def delete(token: Annotated[str, Depends(jwt_required)]):
    """
    A function that deletes the JWT token to the database blocklist.
    """
    with Session(engine) as session:
        session.add(
            TokenBlocklist(jti=token["jti"], 
                           created_at=datetime.now(timezone.utc))
            )
        session.commit()
    return {"message": "Denied"}


@auth.post("/refresh")
async def post(current_user: Annotated[User, Depends(login_required)]):
    """
    Generate a new access token for the authenticated user.
    """
    with Session(engine) as session:
        user = session.get(User, current_user.id)
        if user and not user.blocked and not user.deleted:
            return {
                "access_token": create_token(user.id, "access"),
            }
        return {"access_token": ""}, 401


async def ldap_auth(user_name, password):
    """
    Authenticates a user against an LDAP server.

    Args:
        user_name (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        dict or None: A dictionary containing the user's full name and email if the authentication is successful.
                     None if the authentication fails.
    """
    ldap_user_name = user_name.strip()
    server = Server("ldap://ldap.forumsys.com:389", get_info=ALL)
    connection = Connection(
        server,
        user="uid={},dc=example,dc=com".format(ldap_user_name),
        password=password,
    )
    if connection.bind():
        connection.search(
            "dc=example,dc=com",
            f"(uid={ldap_user_name})",
        )
        if connection.entries:
            return {
                "fullname": connection.entries[0].cn.value,
                "email": connection.entries[0].mail.value,
            }
    else:
        return None
