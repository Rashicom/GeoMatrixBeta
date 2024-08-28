from sqlalchemy.orm import Session
from geomatrix.authorization.schemas import CreateUserRequestModel
from geomatrix.authorization.models import User, APIKeys
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
    return db.query(User).filter(User.id == pk).first()

def get_user_by_email(db:Session, email: str):
    return db.query(User).filter(User.email == email).first()

def activate_user(db:Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user

def get_api_keys(db:Session, user_id:uuid):
    return db.query(APIKeys).filter(APIKeys.user_id == user_id).all()


def get_api_keys_count(db:Session, user_id:uuid) -> int:
    return db.query(APIKeys).filter(APIKeys.user_id == user_id).count()

def create_api_key(db:Session, user_id:uuid):
    """
    Create a api key table row, key is defaultly generated
    set primery key as user_uuid
    """
    new_api_key = APIKeys(user_id = user_id)
    db.add(new_api_key)

    try:
        db.commit()
        db.refresh(new_api_key)
        return new_api_key
    except Exception as e:
        db.rollback()
        raise e
    
def remove_api_key(db, api_key_id):
    api_key = db.query(APIKeys).filter(APIKeys.id == api_key_id).first()
    if not api_key:
        raise Exception("API key not found")
    db.delete(api_key)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e