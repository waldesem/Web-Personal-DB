"""PyDantic models."""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import Annotated, Literal, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)

from app.classes.classes import Roles


class AuthResponse(BaseModel):
    """Tokens."""

    message: Literal["success", "denied", "updated", "delete"]
    access_token: str | None = None
    refresh_token: str | None = None


class AuthLogin(BaseModel):
    """Pydantic model for login form."""

    model_config = ConfigDict(str_max_length=255, regex_engine="python-re")

    username: Annotated[str, AfterValidator(lambda v: v.lower())]
    password: str


class UpdateLogin(AuthLogin):
    """Pydantic model for login form."""

    new_pswd: Annotated[
        str,
        Field(pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$"),
    ]

    @model_validator(mode="after")
    def check_password(self) -> Self:
        """Check passwords combinations."""
        if self.password == self.new_pswd:
            msg = "Новый пароль не должен совпадать со старым"
            raise ValueError(msg)
        return self


class UserForm(BaseModel):
    """Pydantic model for user form."""

    model_config = ConfigDict(
        use_enum_values=True,
        str_strip_whitespace=True,
        str_max_length=255,
    )

    fullname: str
    username: Annotated[str, AfterValidator(lambda v: v.lower())]
    email: EmailStr
    role: Annotated[Roles | None, Field(Roles.guest.value)]


class Session(UserForm):
    """Pydantic model for session."""

    id: int


class User(Session):
    """Pydantic model for user form."""

    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int
    created_at: datetime
    updated_at: datetime


class Actions(BaseModel):
    """Pydantic model for user actions form."""

    model_config = ConfigDict(use_enum_values=True)

    item: Literal["reset", "block", "delete"] | Roles
