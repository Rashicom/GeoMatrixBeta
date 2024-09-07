from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, status, Request
from uuid import UUID

from geomatrix.authorization.crud import get_user_by_api_key
from geomatrix.database.core import async_db

api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="API-Key Authentication",
    description="All the request must be contained a valied API key in the header",
    auto_error=True, # automatically send error to client if not api key set in header
)

async def validate_apikey(request:Request ,db: async_db, api_key: str = Depends(api_key_header)):
    """
    Validate all the request apikey from the header, if not provided automatically returns error(auto_error=True)
    If invalied api key, returns error to client
    if valid api key:
        set request.scope['user'] = user
    """
    # TDOD: impliment db connection
    try:
        user = await get_user_by_api_key(db,api_key)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate API key")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    request.scope["user"] = user
    