from pydantic import BaseModel
from uuid import UUID
from geomatrix.authorization.enums import RoleEnums

class UserModel(BaseModel):
    id: UUID
    name: str
    email: str
    password: str
    role: RoleEnums
    is_active: bool

class CreateUserRequestModel(BaseModel):
    name: str
    email: str
    password: str
    role: RoleEnums

class CreateUserResponseModel(BaseModel):
    id: UUID
    name: str
    email: str
    role: RoleEnums
    is_active: bool

class LoginRequestModel(BaseModel):
    email: str
    password: str

class LoginResponsetModel(BaseModel):
    access_token: str

class ApiKeyResponseSchema(BaseModel):
    id: UUID
    api_key: UUID