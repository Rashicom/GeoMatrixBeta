from sqlalchemy import Column, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from passlib.context import CryptContext

from geomatrix.database.core import Base
from geomatrix.models import TimeStampMixin
from geomatrix.authorization.enums import RoleEnums

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

    # relation with api key table
    api_key_set = relationship("APIKeys", back_populates="user")

    def set_password(self, password: str) -> None:
        """Sets the password for the user."""
        self.password = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored password."""
        return pwd_context.verify(password, self.password)
    

class APIKeys(Base, TimeStampMixin):
    """
    A user can have a limited number of API keys
    """
    __tablename__ = 'api_keys'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.uuid', ondelete='CASCADE'), nullable=False)
    api_key = Column(String, nullable=False, unique=True)

    # relation with user table
    user = relationship("User", back_populates="api_key_set")