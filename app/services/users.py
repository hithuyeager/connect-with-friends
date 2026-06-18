import asyncpg
from fastapi import Request
from authlib.integrations.base_client.errors import OAuthError,TokenExpiredError
from hashlib import sha256

from core.security import (
    oauth,generate_access_token,generate_refresh_token,
    hash_password,verify_password,verify_refresh_token
)
from repositories.users_repo import (
    get_user_by_email,add_app_user,add_google_user,
    get_google_user_by_sub,get_by_username,insert_new_session,
    insert_refresh_token,get_session_info,logout_session
)
from tasks.email_tasks import send_welcome_message
import core.errors as error

def generate_tokens(user_id: str,session_id: str) -> dict:
    access_token = generate_access_token(str(user_id))
    refresh_token = generate_refresh_token(str(user_id),session_id)
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }

async def make_new_session(conn:asyncpg.Connection,user_id: str):
    async with conn.transaction():
        session_id = await insert_new_session(conn,user_id)
        tokens = generate_tokens(user_id,session_id)
        hashed_refresh_token = sha256(tokens["refresh_token"].encode()).hexdigest()
        is_succeed = await insert_refresh_token(conn,session_id,hashed_refresh_token)
        if is_succeed:
            return tokens
        else:
            raise error.DataBaseError()

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
    user = await get_user_by_email(conn,user_email)
    if user:
        return await make_new_session(conn,user["id"])
    new_user_id = await add_google_user(conn,user_email,username,user_sub)
    print("new user id inserted",new_user_id)
    send_welcome_message.delay(user_email,username)
    return make_new_session(conn,new_user_id)

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
    async with conn.transaction():
        user_id = await add_app_user(conn,email,username,hashed_password)
        return await make_new_session(conn,user_id)

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
        return await make_new_session(conn,user_info["id"])

#-------------------UPDATE SESSION----------------------------------
async def token_rotation(
    conn: asyncpg.Connection,
    refresh_token: str,
):
    payload = verify_refresh_token(refresh_token)
    session_info = await get_session_info(conn,payload["session_id"])
    if not session_info["is_active"]:
        raise error.InvalidSession()
    new_hashed_refresh_token = sha256(refresh_token.encode()).hexdigest()
    if new_hashed_refresh_token != session_info["hashed_refresh_token"]:
        raise error.FraudDetection()
    tokens = generate_tokens(payload["sub"],payload["session_id"])
    hashed_refresh_token = sha256(tokens["refresh_token"].encode()).hexdigest()
    is_succeed = await insert_refresh_token(conn,payload["session_id"],hashed_refresh_token)
    if is_succeed:
        return tokens

async def logout_the_session(conn: asyncpg.Connection,refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    await logout_session(conn,payload["session_id"])
    return  