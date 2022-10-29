import datetime

from ninja import Schema
from ninja import Field
from pydantic import EmailStr


class PasswordSchema(Schema):
    password1: str = Field(min_length=6)
    password2: str = Field(min_length=6)


class AccountCreateBody(PasswordSchema):
    name: str = Field(min_length=4)
    email: EmailStr


class AccountLoginBody(Schema):
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(Schema):
    name: str
    email: str


class AccountOut(Schema):
    token: str
    user: UserOut


class PasswordResetToken(Schema):
    token: str


class OtpIn(Schema):
    otp: int = Field(..., ge=1000, le=9999)


class AccountUpdate(Schema):
    name: str = None
    gender: str = None
    phone: str = None
    birth_date: datetime.date = None


class AccountInfo(Schema):
    name: str
    email: EmailStr
    profile: str = None
    gender: str = None
    phone: str = None
    birth_date: datetime.date = None
