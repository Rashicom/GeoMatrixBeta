from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired, BadSignature
from pydantic import EmailStr
from typing import Dict

from geomatrix.config import get_settings
settings = get_settings()

# token algo for creating time stamped and signed tokens for varify email
Email_vafificatin_token_algo = URLSafeTimedSerializer(settings.SECRET_KEY, salt="Email_varification")

def create_url_varification_token(email:EmailStr) -> str:
    """
    return a token which is timestamped and signed
    it include a email to identify user when variy
    """
    return Email_vafificatin_token_algo.dumps(email)

def varify_url_varification_token(token:str) -> Dict:
    """
    this method call with token which is come from other domains
    perform check on the token and confirm the email is valied or not
    """
    try:
        email = Email_vafificatin_token_algo.loads(token)
    except SignatureExpired:
        return {"email": None, "status":"Signature Expired"}
    except BadTimeSignature:
        return {"email": None, "status":"Token time expired"}
    except BadSignature:
        return {"email": None, "status":"Bad Signature"}
    return {"email": email, "status":"OK"}