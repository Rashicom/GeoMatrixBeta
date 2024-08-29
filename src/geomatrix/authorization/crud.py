from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from geomatrix.authorization.schemas import CreateUserRequestModel
from geomatrix.authorization.models import User, APIKeys
import uuid

async def create_user(db:AsyncSession, user_model:CreateUserRequestModel, **kwargs) -> User:
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

    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        await db.rollback()
        raise e

async def get_user_by_uuid(db:Session, pk:uuid):
    result = await db.execute(select(User).filter(User.id == pk))
    return result.scalars().first()

async def get_user_by_email(db:Session, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def activate_user(db:Session, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    user.is_active = True

    try:
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        await db.rollback()
        raise e


async def get_api_keys(db:Session, user_id:uuid):
    result = await db.execute(select(APIKeys).filter(APIKeys.user_id == user_id))
    return result.scalars().all()


async def get_api_keys_count(db:Session, user_id:uuid) -> int:
    result = await db.execute(select(func.count()).where(APIKeys.user_id == user_id))
    return result.scalar_one()

async def create_api_key(db:Session, user_id:uuid):
    """
    Create a api key table row, key is defaultly generated
    set primery key as user_uuid
    """
    new_api_key = APIKeys(user_id = user_id)
    db.add(new_api_key)

    try:
        await db.commit()
        await db.refresh(new_api_key)
        return new_api_key
    except Exception as e:
        await db.rollback()
        raise e


async def remove_api_key(db:AsyncSession, api_key_id):
    result = await db.execute(select(APIKeys).filter(APIKeys.id == api_key_id))
    api_key = result.scalars().first()
    if not api_key:
        raise Exception("API key not found")
    await db.delete(api_key)
    
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
