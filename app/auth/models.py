from typing import Optional
from datetime import datetime
from app.database import engine
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    phone: str = Field(
        unique=True, nullable=False,
        index=True, regex='^[0-9]{10}$'
    )
    password: str = Field(nullable=False, min_length=8)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: bool = Field(default=False, nullable=False)


class UserForm(UserBase):
    otp: str = Field(regex='^[0-9]{4}$')


class Otp(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str = Field(
        unique=True, nullable=False,
        index=True, regex='^[0-9]{10}$'
    )
    otp: str = Field(nullable=False)
    exp: datetime = Field(nullable=False)


class AuthToken(SQLModel):
    access_token: str


SQLModel.metadata.create_all(engine)
