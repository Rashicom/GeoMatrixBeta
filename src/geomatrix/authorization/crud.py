from sqlalchemy.orm import Session
from geomatrix.authorization.schemas import CreateUserRequestModel
from geomatrix.authorization.models import User
import uuid

def create_user(db:Session, user_model:CreateUserRequestModel, **kwargs) -> User:
    """
    For creating a new user
    kwargs can pass while user creation for override values
    like create_user(db,user_model,role="Public")
    """
    user_data = user_model.model_dump()
    user_data.update(kwargs)
    new_user = User(**user_data)
    new_user.set_password(user_data.get("password"))

    # save user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_uuid(db:Session, pk:uuid):
    return db.query(User).filter(User.uuid == pk).first()

def get_user_by_email(db:Session, email: str):
    return db.query(User).filter(User.email == email).first()

def activate_user(db:Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user