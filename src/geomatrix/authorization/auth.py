from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    return pwd_context.hash(password)

