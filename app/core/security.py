from jose import JWTError,jwt,ExpiredSignatureError

from config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire
REFRESH_TOKEN_EXPIRE = settings.refresh_token_expire

async def generate_access_token():