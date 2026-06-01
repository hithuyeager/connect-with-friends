from jose import JWTError,jwt,ExpiredSignatureError
from uuid import UUID
from datetime import datetime,timedelta,timezone

from config import settings
import errors as error

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire
REFRESH_TOKEN_EXPIRE = settings.refresh_token_expire

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
    

