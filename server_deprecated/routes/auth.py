from datetime import datetime, timezone
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Response
from ldap3 import ALL, Connection, Server
from sqlmodel import Session, select

from ..dependencies import create_token, jwt_required, login_required
from ..models.model import TokenBlocklist, User, engine
from ..models.schema import LoginSchema, TokenSchema, UserWithRoles

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.get("/", status_code=200)
async def get_auth(
    current_user: Annotated[User, Depends(login_required)],
) -> UserWithRoles:
    """
    Retrieves the current authenticated user from the database.

    This function is called when the '/auth' endpoint is accessed with the
    GET method. It returns the currently authenticated user and their roles.

    Parameters
    ----------
    current_user : User
        The currently authenticated user.

    Returns
    -------
    UserWithRoles
        A JSON object containing the user and their roles.
    """

    # Calculate the time delta between the current time and when the password
    # was last changed
    delta_change = datetime.now(timezone.utc) - current_user.pswd_created

    # Open a session with the database
    with Session(engine) as session:
        # If the user is blocked, not deleted, and the password has not been
        # changed in the last year, then update the user's last login time
        if (
            not current_user.blocked
            and not current_user.deleted
            and delta_change.days < 365
        ):
            current_user.last_login = datetime.now(timezone.utc)
            # Commit the changes to the database
            session.commit()
            # Return the user and their roles
            return {
                "user": current_user,
                "roles": current_user.roles,
            }
        # If the user does not meet the above conditions, then return a 401
        # Unauthorized response
        raise HTTPException(status_code=401)


@auth.post("/login", status_code=201)
async def post_login(json_data: LoginSchema) -> TokenSchema:
    """
    Post method for the given API endpoint.

    Parameters
    ----------
    json_data : LoginSchema
        The JSON data sent in the request body.

    Returns
    -------
    TokenSchema
        A JSON object containing a message and the authentication tokens.
    """
    with Session(engine) as session:
        # Get the user from the database
        user = session.exec(
            select(User).where(User.username == json_data.username)
        ).one_or_none()

        if user and not user.blocked and not user.deleted:
            # Check if the password is correct
            if bcrypt.checkpw(json_data.password.encode("utf-8"), user.password):
                # Calculate the time delta between the current time and when the password
                # was last changed
                delta_change = datetime.now(timezone.utc) - user.pswd_created

                # If the password has not been changed in the last year, then update the user's last
                # login time and set the change password flag to False
                if not user.change_pswd and delta_change.days < 365:
                    user.last_login = datetime.now(timezone.utc)
                    user.change_pswd = False
                    user.attempt = 0
                    session.commit()
                    return {
                        "access_token": create_token(str(user.id), "access"),
                        "refresh_token": create_token(str(user.id), "refresh"),
                    }
                # If the password has been changed in the last year, then return a message
                # indicating that the password is overdue
                return Response(status_code=202)
            else:
                # If the password is incorrect, then increment the user's attempt count
                # If the attempt count is equal to 9, then block the user
                if user.attempt < 9:
                    user.attempt += 1
                else:
                    user.blocked = True
                session.commit()

        return Response(status_code=203)

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


@auth.patch("/login", status_code=201)
async def patch_password(json_data: LoginSchema) -> dict[str, str]:
    """
    Patch method for updating user password.

    Args:
        json_data (LoginSchema): The JSON data sent in the request body.

    Returns:
        dict[str, str]: A JSON object containing a message.

    Raises:
        None.
    """
    with Session(engine) as session:
        # Get the user from the database
        user = session.exec(
            select(User).where(User.username == json_data.username)
        ).one_or_none()

        if (
            # If the user exists and is not blocked
            user
            and not user.blocked
            # And the provided password is correct
            and bcrypt.checkpw(json_data.password.encode("utf-8"), user.password)
        ):
            # Update the user's password
            user.password = bcrypt.hashpw(
                json_data.new_pswd.encode("utf-8"), bcrypt.gensalt()
            )

            # Set the change password flag to False
            user.change_pswd = False

            # Commit the changes to the database
            session.commit()

            # Return a message indicating that the password has been changed
            return Response(status_code=205)

        # If any of the conditions are not met, return a message indicating that the password
        # change was denied
        return Response(status_code=203)


@auth.delete("/login", status_code=204)
async def delete(token: Annotated[str, Depends(jwt_required)]):
    """
    Deletes the JWT token to the database blocklist.

    This function is used to block the JWT token from being used again by adding it to the
    token blocklist table in the database.

    Parameters
    ----------
    token : str
        The JWT token to be blocked.

    Returns
    -------
    dict[str, str]
        A JSON object containing a message indicating that the token has been blocked.
    """
    with Session(engine) as session:
        # Add the JWT token to the token blocklist table
        session.add(
            TokenBlocklist(jti=token["jti"], created_at=datetime.now(timezone.utc))
        )
        # Commit the changes to the database
        session.commit()
    # Return a message indicating that the token has been blocked
    return Response(status_code=204)


@auth.post("/refresh", status_code=201)
async def get_refresh_token(current_user: Annotated[User, Depends(login_required)]):
    """
    Generates a new access token for the authenticated user.

    This endpoint is used to refresh an access token for an authenticated user.
    It checks if the user is not blocked and not deleted, and if the password
    has not been changed in the last year. If any of these conditions are met, then
    a new access token is generated and returned.

    Parameters
    ----------
    current_user : User
        The currently authenticated user.

    Returns
    -------
    dict[str, str]
        A JSON object containing the new access token.
    """
    delta_change = datetime.now(timezone.utc) - current_user.pswd_created
    if (
        # Check if the user is not blocked and not deleted
        not current_user.blocked
        # And the password has not been changed in the last year
        and not current_user.deleted
        and delta_change.days < 365
    ):
        # Generate a new access token
        return {
            "access_token": create_token(current_user.id, "access"),
        }
    # If any of the conditions are not met, return an empty access token
    return Response(status_code=401)


async def ldap_auth(user_name: str, password: str) -> dict | None:
    """
    Authenticates a user against an LDAP server.

    This function is used to authenticate a user against an LDAP server.
    It takes the username and password as arguments, and returns a dictionary
    containing the user's full name and email if the authentication is successful.
    If the authentication fails, it returns None.

    Parameters
    ----------
    user_name : str
        The username of the user to authenticate.
    password : str
        The password of the user to authenticate.

    Returns
    -------
    dict or None
        A dictionary containing the user's full name and email if the authentication is successful.
        None if the authentication fails.
    """
    # Strip any leading or trailing whitespace from the username
    ldap_user_name = user_name.strip()

    # Create an LDAP server object
    server = Server("ldap://ldap.forumsys.com:389", get_info=ALL)

    # Create an LDAP connection object
    connection = Connection(
        server,
        # The user's DN is in the format "uid=<username>,dc=example,dc=com"
        user="uid={},dc=example,dc=com".format(ldap_user_name),
        # The password to use for the connection
        password=password,
    )

    # Attempt to bind to the LDAP server
    if connection.bind():
        # Search for the user's entry in the LDAP directory
        connection.search(
            # The base DN to search from
            "dc=example,dc=com",
            # The filter to use for the search
            f"(uid={ldap_user_name})",
        )

        # If the search returned any entries, return the user's full name and email
        if connection.entries:
            return {
                "fullname": connection.entries[0].cn.value,
                "email": connection.entries[0].mail.value,
            }
    else:
        # If the authentication failed, return None
        return None
