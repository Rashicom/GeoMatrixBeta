from pydantic import BaseModel
from uuid import UUID
from geomatrix.authorization.enums import RoleEnums
from typing import Literal

class UserModel(BaseModel):
    uuid: UUID
    name: str
    email: str
    password: str
    role: Literal["government","government_agencies","public"]
    is_active: bool

class CreateUserRequestModel(BaseModel):
    name: str
    email: str
    password: str
    role: RoleEnums

class CreateUserResponseModel(BaseModel):
    uuid: UUID
    name: str
    email: str
    role: RoleEnums
    is_active: bool

class LoginRequestModel(BaseModel):
    email: str
    password: str

class LoginResponsetModel(BaseModel):
    access_token: str