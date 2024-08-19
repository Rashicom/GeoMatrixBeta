from geomatrix.database.core import Base
from geomatrix.models import TimeStampMixin

from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID

import uuid
from geomatrix.authorization.enums import RoleEnums
import bcrypt
from passlib.context import CryptContext

from geomatrix.authorization.auth import hash_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# All authorization tables
class User(Base, TimeStampMixin):
    __tablename__ = 'users'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnums), nullable=False)
    is_active = Column(Boolean, default=True)

    def set_password(self, password: str) -> None:
        """Sets the password for the user."""
        self.password = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored password."""
        return pwd_context.verify(password, self.password)