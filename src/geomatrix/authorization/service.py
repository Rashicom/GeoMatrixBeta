from fastapi import status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
import uuid

from geomatrix.authorization.schemas import CreateUserRequestModel, LoginRequestModel
from geomatrix.authorization.crud import create_user, get_user_by_email, activate_user, get_api_keys_count, create_api_key, get_api_keys, remove_api_key
from geomatrix.authorization.enums import RoleEnums
from geomatrix.common.email import send_template_mail
from geomatrix.common.schemas import HtmlEmailSchema
from geomatrix.authorization.utils import create_url_varification_token,varify_url_varification_token
from geomatrix.config import get_settings

settings = get_settings()

async def register_geomatrix_user(db: AsyncSession, user_model:CreateUserRequestModel, backround_task: BackgroundTasks):
    """
    This method is registering geomatric user
    here check all the user precreation constrains, we create if all pass, else rise corresponding error response
    return user object if successful else return None
    """

    # check if user already exists, return user already exixt response
    if await get_user_by_email(db, user_model.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )
    
    try:
        # user must be inactive state initially
        new_user = await create_user(db, user_model,is_active=False)
        
        # send varification mail to activate user
        # send verification email as a backround task
        url_token = create_url_varification_token(user_model.email)
        activation_url = f"{settings.BASE_URL}/auth/varify_email/{url_token}"
        email_schema = HtmlEmailSchema(
            subject="Verify your Geomatrix Account",
            recipients=[user_model.email],
            template_body={
                "activation_url": activation_url,
            },
        )
        backround_task.add_task(send_template_mail,email_schema)
        # send_template_mail(email_schema)
        return new_user
    except Exception as e:
        print("Issue with pydentic model",e)
        db.rollback()
        return None


async def is_authenticated(db:AsyncSession, login_form:OAuth2PasswordRequestForm):
    """
    Authenticate user using the email and password
    retrun user if authenticated, else return None
    """
    user = await get_user_by_email(db, login_form.username)
    if user:
        if user.check_password(login_form.password):
            if user.is_active:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is in inactive state, contact us")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalied user")
    

async def varify_email_by_token(db:AsyncSession,token:str):
    """
    Varify the token is valied or not
    if valied extracted email from the token can be activated
    else reject
    """
    varification_resp = varify_url_varification_token(token)
    email = varification_resp["email"]
    if email is not None:
        user = await activate_user(db,varification_resp["email"])
        return user
    else:
        return None
    

async def generate_api_key(db:AsyncSession,user_id:uuid):
    """
    Generate unique API key for authenticated user
    A user can only can have perticular number of api keys
    """
    # ensure the user cannot have more than limit api keys
    api_key_count = await get_api_keys_count(db, user_id)
    if api_key_count >= settings.MAX_API_KEYS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has reached the limit of API keys")
    
    try:
        new_api_key = await create_api_key(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cant create API Key")
    return new_api_key


async def get_users_apikeys(db:AsyncSession, user_id:uuid):
    """
    Fetch all api keys of a user
    """
    api_keys = await get_api_keys(db,user_id)
    return api_keys

async def delete_api_key(db:AsyncSession, api_key_id):
    """
    Delete a specific api key
    """
    try:
        await remove_api_key(db, api_key_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API Key Not Found")
    