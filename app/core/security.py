from jose import JWTError,jwt,ExpiredSignatureError
from uuid import UUID
from datetime import datetime,timedelta,timezone
from authlib.integrations.starlette_client import OAuth
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError,InvalidHashError,HashingError
from asyncio import to_thread

from config import settings
from . import errors as error

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire
REFRESH_TOKEN_EXPIRE = settings.refresh_token_expire

oauth = OAuth()

oauth.register(
    name = "google",
    client_id = settings.google_client_id,
    client_secret = settings.google_client_secret,
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs = {
        "scope": "openid email profile"
    }
)
#---------------------------GENERATING TOKENS--------------------------------------
def generate_access_token(user_id: str) -> str:
    payload = {
        "sub" : user_id,
        "exp" : datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE),
        "type" : "access"
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def generate_refresh_token_token(user_id: str) -> str:
    payload = {
        "sub" : user_id,
        "exp" : datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE),
        "type" : "refresh"
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

#--------------------VERIFYING THE TOKENS----------------------------------------
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise error.InvalidTokenTypeError()
        return payload
    except ExpiredSignatureError:
        raise error.TokenExpiredError()
    except JWTError:
        raise error.InvalidTokenError()

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise error.InvalidTokenTypeError()
        return payload
    except ExpiredSignatureError:
        raise error.TokenExpiredError()
    except JWTError:
        raise error.InvalidTokenError()
    
#------------------PASSWORD HASHER-----------------------------------

ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)
async def hash_password(raw_password: str) -> str:
    try:
        return await to_thread(ph.hash,raw_password)
    except HashingError:
        raise error.HashingError()

async def verify_password(hashed_password: str,raw_password: str):
    try:
        return await to_thread(ph.verify,hashed_password,raw_password)
    except VerifyMismatchError:
        raise error.WrongPasswordError()
    except InvalidHashError:
        raise error.InvalidHashError()
    