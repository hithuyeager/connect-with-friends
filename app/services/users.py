import asyncpg
from fastapi import Request
from authlib.integrations.base_client.errors import OAuthError,TokenExpiredError

from core.security import (
    oauth,generate_access_token,generate_refresh_token,
    hash_password,verify_password
)
from repositories.users_repo import (
    get_user_by_email,add_app_user,add_google_user,
    get_google_user_by_sub,get_by_username
)
from tasks.email_tasks import send_welcome_message
import core.errors as error

def generate_tokens(user_id: str) -> dict:
    access_token = generate_access_token(str(user_id))
    refresh_token = generate_refresh_token(str(user_id))
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }

#------------------GOOGLE UTILS-----------------------------------------
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request,redirect_uri,prompt="select_account")

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

#--------------------SIGNUP GOOGLE ROUTE FUNCTION----------------------
async def user_google_login(request: Request,conn: asyncpg.Connection):
    user_info = await callback_url(request)
    user_email = user_info.get("email")
    user_sub = user_info.get("sub")
    username = user_info.get("name","")
    user_id = await get_google_user_by_sub(conn,user_sub)
    if user_id:
        print("fetched from db and got it")
        return generate_tokens(str(user_id))
    new_user_id = await add_google_user(conn,user_email,username,user_sub)
    print("new user id inserted",new_user_id)
    send_welcome_message.delay(user_email,username)
    return generate_tokens(str(new_user_id))

#------------------APP SIGNUP--------------------------------------------
async def app_sign_up(
    conn: asyncpg.Connection,
    email: str,
    username: str,
    password: str):
    email_exist = await get_user_by_email(conn,email)
    if email_exist:
        raise error.EmailAlreadyExistError()
    username_exist = await get_by_username(conn,username)
    if username_exist:
        raise error.UsernameExistError()
    hashed_password = await hash_password(password)
    user_id = await add_app_user(conn,email,username,hashed_password)
    return generate_tokens(user_id)

async def app_sign_in(
    conn: asyncpg.Connection,
    email: str,
    password: str
):
    user_info = await get_user_by_email(conn,email)
    if not user_info:
        raise error.EmailNotExistError()
    if user_info["sign_up_type"] == "google login":
        raise error.GoogleUserError()
    if await verify_password(user_info["password"],password):
        return generate_tokens(user_info["id"])
    