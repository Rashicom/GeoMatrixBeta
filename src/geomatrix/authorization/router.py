from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from geomatrix.database.core import get_db
from geomatrix.authorization.service import register_geomatrix_user
from geomatrix.authorization.schemas import CreateUserRequestModel, CreateUserResponseModel

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