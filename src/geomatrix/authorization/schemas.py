from pydantic import BaseModel
from uuid import UUID


class UserModel(BaseModel):
    uuid: UUID
    name: str
    email: str
    password: str
    role: str
    is_active: bool

class CreateUserRequestModel(BaseModel):
    name: str
    email: str
    password: str
    role: str

class CreateUserResponseModel(UserModel):
    pass

class LoginRequestModel(BaseModel):
    email: str
    password: str

class LoginResponsetModel(BaseModel):
    acess_token: str