from repositories.users_repo import (
    get_user_by_email,add_app_user,add_google_user,
    get_google_user_by_sub
)
import asyncpg
from fastapi import Request
from authlib.integrations.base_client.errors import OAuthError,TokenExpiredError

from core.security import (
    oauth,generate_access_token,generate_refresh_token_token
)
import core.errors as error

def generate_tokens(user_id: str) -> dict:
    access_token = generate_access_token(user_id)
    refresh_token = generate_refresh_token_token(user_id)
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }

#------------------GOOGLE UTILS-----------------------------------------
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request,redirect_uri)

async def callback_url(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except TokenExpiredError:
        raise error.GoogleTokenExpiredError()
    except OAuthError:
        raise error.GoogleTokenError()
    user_info = token.get("userinfo")

    if (not user_info) or (not user_info.get("email")):
        raise error.GoogleLoginError()
    return user_info

#--------------------SIGNUP ROUTE FUNCTION----------------------
async def user_google_login(request: Request,conn: asyncpg.Connection):
    user_info = await callback_url(request)
    user_email = user_info.get("email")
    user_sub = user_info.get("sub")
    username = user_info.get("name","")
    user_id = str(await get_google_user_by_sub(conn,user_sub))
    if user_id:
        return generate_tokens(user_id)
    new_user_id = await add_google_user(conn,user_email,username,user_sub)
    return generate_tokens(str(new_user_id))
        


