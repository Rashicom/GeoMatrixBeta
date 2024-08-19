from pydantic import BaseModel
from uuid import UUID

class CreateUserRequestModel(BaseModel):
    name: str
    email: str
    password: str
    role: str

class CreateUserResponseModel(BaseModel):
    uuid: UUID
    name: str
    email: str
    password: str
    role: str
    is_active: bool