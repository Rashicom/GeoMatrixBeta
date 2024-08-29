from passlib.context import CryptContext
from typing import Annotated
from datetime import timedelta, datetime
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from geomatrix.authorization.models import User
from geomatrix.authorization.schemas import UserModel
from geomatrix.config import get_settings
from geomatrix.database.core import async_db
from geomatrix.authorization.crud import get_user_by_uuid

settings = get_settings()

def create_access_token(user_model:User):
    secret_key=settings.SECRET_KEY
    algorithm=settings.ALGORITHM
    expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    to_encode = {
        "sub": str(user_model.id)
    }
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=expires_delta)
    else:
        # default expires in 30
        expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,secret_key, algorithm=algorithm)
    return encoded_jwt


auth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
async def get_current_user(db:async_db,token:str=Depends(auth2_schema)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    
    # check if token is expired or not
    if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    # find the user and return if found and active else rise user not found exception
    
    user_pk = payload.get("sub")
    user = await get_user_by_uuid(db, pk=user_pk)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # inactive user
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is in inactive state, contact GeoMatrix")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]