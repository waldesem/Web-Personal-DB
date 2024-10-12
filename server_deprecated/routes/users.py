from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from backend.models.schema import UserWithRoles

from ..config import settings
from ..dependencies import Permission
from ..models.classes import Roles
from ..models.model import engine, User, Role


usr = APIRouter(prefix="/users", tags=["users"])


@usr.get(
    "/",
    status_code=200,
    dependencies=[Depends(Permission(roles=[Roles.admin.value]))],
)
async def get_users(searches: str = None) -> list[User]:
    """
    Endpoint to handle requests for getting users.
    """
    with Session(engine) as session:
        if searches:
            query = select(User).filter(User.username.contains(searches))
        else:
            query = select(User)
        return session.exec(query.order_by(User.id.asc())).all()


@usr.get("/user/{user_id}", status_code=200)
async def get_user(
    user_id,
    current_user: Annotated[User, Depends(Permission(roles=[Roles.admin.value]))],
    action: str = None,
) -> UserWithRoles:
    """
    Retrieves a user based on the specified action and user ID.
    """
    with Session(engine) as session:
        if action != "view":
            user = session.get(User, user_id)
            match action:
                case "block":
                    if user.username != current_user.username:
                        user.blocked = not user.blocked
                case "drop":
                    user.password = bcrypt.hashpw(
                        settings.default_password.encode("utf-8"),
                        bcrypt.gensalt(),
                    )
                    user.attempt = 0
                    user.change_pswd = True
                case _:
                    user.region_id = action
            session.commit()
        user = session.get(User, user_id)
        return {
            "user": user,
            "roles": user.roles,
        }

@usr.post(
    "/user",
    status_code=204,
    dependencies=[Depends(Permission(roles=[Roles.admin.value]))],
)
async def post_user(json_data: User):
    """
    Creates a new user based on the provided JSON data.
    """
    with Session(engine) as session:
        if not session.exec(
                select(User).filter_by(username=json_data.username)
            ).one_or_none():
            session.add(
                User(
                    fullname=json_data.fullname,
                    username=json_data.username,
                    email=json_data.email,
                    region_id=json_data.region_id,
                    password=bcrypt.hashpw(
                        settings.default_password.encode("utf-8"),
                        bcrypt.gensalt(),
                    ),
                )
            )
            session.commit()
            return {"message": "Created"}
        raise HTTPException(status_code=409)


@usr.patch(
    "/user/{user_id}",
    status_code=204,
    dependencies=[Depends(Permission(roles=[Roles.admin.value]))],
)
async def patch_user(user_id, json_data: User):
    """
    Patch a user's information.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            for key, value in json_data.__dict__.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            session.commit()
            return {"message": "Changed"}
        raise HTTPException(status_code=403)


@usr.delete("/user/{user_id}", status_code=204)
async def delete_user(
    user_id,
    current_user: Annotated[User, Depends(Permission(roles=[Roles.admin.value]))],
):
    """
    Delete a user by their ID.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user and user.username != current_user.username:
            user.deleted = True
            session.commit()
            return Response(status_code=204)
        raise HTTPException(status_code=403)


@usr.get(
    "/role/{value}/{user_id}",
    dependencies=[Depends(Permission(roles=[Roles.admin.value]))],
)
async def get_role(value, user_id):
    with Session(engine) as session:
        user = session.get(User, user_id)
        role = session.get(Role, value)
        if user and role not in user.roles:
            user.roles.append(role)
            session.commit()
            return Response(status_code=201)
        raise HTTPException(status_code=403)


@usr.delete("/role/{value}/{user_id}")
async def delete_role(
    value,
    user_id,
    current_user: Annotated[User, Depends(Permission(roles=[Roles.admin.value]))],
):
    """
    Deletes a role from a user.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        role = session.get(Role, value)
        if (
            user
            and role
            and (
                user.username != current_user.username or role.role != Roles.admin.value
            )
        ):
            user.roles.remove(role)
            session.commit()
            return Response(status_code=204)
        raise HTTPException(status_code=403)

