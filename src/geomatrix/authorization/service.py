from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from geomatrix.authorization.schemas import CreateUserRequestModel, LoginRequestModel
from geomatrix.authorization.crud import create_user, get_user_by_email
from geomatrix.authorization.enums import RoleEnums


def register_geomatrix_user(db: Session, user_model:CreateUserRequestModel):
    """
    This method is registering geomatric user
    here check all the user precreation constrains, we create if all pass, else rise corresponding error response
    return user object if successful else return None
    """

    # check if user already exists, return user already exixt response
    if get_user_by_email(db, user_model.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )
    
    try:
        # user must be in inactive state if role is not public
        if user_model.role != RoleEnums.PUBLIC:
            return create_user(db, user_model,is_active=False)
        else:
            # default is_active=True
            return create_user(db, user_model)
    except Exception as e:
        print(e)
        db.rollback()
        return None


def is_authenticated(db:Session, user_model:LoginRequestModel):
    """
    Authenticate user using the email and password
    retrun user if authenticated, else return None
    """
    user = get_user_by_email(db, user_model.email)
    if user:
        if user.check_password(user_model.password):
            if user.is_active:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is in inactive state, contact us")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalied user")
    
