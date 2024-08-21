from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from geomatrix.database.core import get_db
from geomatrix.authorization.service import register_geomatrix_user, is_authenticated
from geomatrix.authorization.auth import CurrentUser,create_access_token
from geomatrix.authorization.schemas import CreateUserRequestModel, CreateUserResponseModel, LoginRequestModel, LoginResponsetModel, UserModel

router = APIRouter()

@router.post("/signup", response_model=CreateUserResponseModel)
def sign_up(user_request_model: CreateUserRequestModel, db: Session=Depends(get_db)):
    """
    Endpoint for user registration
    """
    # logic for user registration goes here
    user = register_geomatrix_user(db, user_request_model) # duplicate user exception internaly handled and returns
    if user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    return user


@router.post("/login", response_model=LoginResponsetModel)
def login(login_model:OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    """
    Returns jwt token for authenticated users
    """
    user = is_authenticated(db,login_model) # exception rised internally

    # generate jwt token
    jwt_token =  create_access_token(user)
    return {"access_token":jwt_token}


@router.get("/protected")
def protedted(user:CurrentUser):
    print("Logined user",user.email)
    return {"status":"protected resources"}
