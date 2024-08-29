from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

from geomatrix.database.core import async_db
from geomatrix.authorization.service import register_geomatrix_user, is_authenticated, varify_email_by_token, generate_api_key, get_users_apikeys, delete_api_key
from geomatrix.authorization.auth import CurrentUser,create_access_token
from geomatrix.authorization.schemas import CreateUserRequestModel, CreateUserResponseModel, LoginResponsetModel, ApiKeyResponseSchema

router = APIRouter()

@router.post("/signup", response_model=CreateUserResponseModel)
async def sign_up(user_request_model: CreateUserRequestModel,backround_task:BackgroundTasks, db: async_db):
    """
    Endpoint for user registration
    """
    # logic for user registration goes here
    user = await register_geomatrix_user(db, user_request_model, backround_task) # duplicate user exception internaly handled and returns
    if user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    return user


@router.post("/login", response_model=LoginResponsetModel)
async def login(db: async_db,login_model:OAuth2PasswordRequestForm=Depends()):
    """
    Returns jwt token for authenticated users
    """
    user = await is_authenticated(db,login_model) # exception rised internally

    # generate jwt token
    jwt_token =  create_access_token(user)
    return {"access_token":jwt_token}


@router.get("/varify_email/{token}")
async def varify_email(token:str, db: async_db):
    """
    Varify email by token
    """
    # TODO: redirect to the appropreate pages according to the response
    # TODO: in case of invalied token, next flow?
    user = await varify_email_by_token(db,token)
    if user is None:
        return {"Status":"Account rejected"}
    else:
        return {"Status":"Account activated"}


@router.get("/create_apikey", response_model=ApiKeyResponseSchema)
async def create_new_api_key(user:CurrentUser,db: async_db):
    """
    Generate API key for authenticated user
    """
    new_api_key = await generate_api_key(db, user.id)
    return new_api_key


@router.get("/my_apikeys", response_model=List[ApiKeyResponseSchema])
async def get_my_apikeys(user:CurrentUser, db: async_db):
    """
    Retrurns all api keys for the current user
    """
    api_keys = await get_users_apikeys(db,user.id)
    return api_keys

@router.delete("/api/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_apikey(api_key_id,user:CurrentUser, db:async_db):
    """
    Delete an API key for the current user
    """
    await delete_api_key(db,api_key_id)
    return

@router.get("/protected")
async def protedted(user:CurrentUser):
    print("Logined user",user.email)
    return {"status":"protected resources"}
