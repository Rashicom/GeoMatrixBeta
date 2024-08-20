from passlib.context import CryptContext
from typing import Union
from datetime import timedelta, datetime
import jwt

from geomatrix.authorization.models import User
from geomatrix.config import get_jwt_settings

jwt_settings = get_jwt_settings()

def create_access_token(user_model:User):
    secret_key=jwt_settings.SECRET_KEY
    algorithm=jwt_settings.ALGORITHM
    expires_delta=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    to_encode = {
        "sub": str(user_model.uuid)
    }
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=expires_delta)
    else:
        # default expires in 30
        expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,secret_key, algorithm=algorithm)
    return encoded_jwt



def get_user_by_token():
    pass