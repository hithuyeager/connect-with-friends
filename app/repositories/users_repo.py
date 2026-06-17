import asyncpg

from uuid import UUID

async def get_user_by_email(
    conn: asyncpg.Connection,
    email: str
    ):
    user = await conn.fetchrow(
        """SELECT id,email,username,sign_up_type,password 
         FROM users WHERE email = $1""",
         email
    )
    return dict(user) if user else None
    
async def get_by_username(
    conn: asyncpg.Connection,
    username: str
):
    user = await conn.fetchval(
        "SELECT id FROM users WHERE username = $1",
        username
    )
    return user


async def add_app_user(
    conn: asyncpg.Connection,
    email: str,
    username: UUID,
    password: str,
    sign_up_type: str = "app login"
):
    return await conn.fetchval(
        """ INSERT INTO  users 
        (email,username,password,sign_up_type) 
        values ($1,$2,$3,$4) RETURNING id""",
        email,username,password,sign_up_type
    )
    
async def add_google_user(
        conn: asyncpg.Connection,
        email: str,
        username: str,
        google_sub: str,
        sign_up_type: str = "google login"
) :
    return await conn.fetchval(
        """INSERT INTO users 
        (email,username,google_sub,sign_up_type) 
        values ($1,$2,$3,$4) RETURNING id""",
        email,username,google_sub,sign_up_type
    )

async def get_google_user_by_sub(
        conn: asyncpg.Connection,
        google_sub: str
):
    return await conn.fetchval(
        "SELECT id FROM users WHERE google_sub = $1",
        google_sub
    )

async def get_session_info(
    conn: asyncpg.Connection,
    session_id: str
):
    info = await conn.fetchrow(
    """SELECT session_id,user_id,hashed_refresh_token,is_active 
    FROM sessions WHERE session_id = $1
    """,session_id
    )
    if info:
        return {
            "session_id" : str(info["session_id"]),
            "user_id" : str(info["user_id"]),
            "hashed_refresh_token" : info["hashed_refresh_token"],
            "is_active" : bool(info["is_active"])
        }
    return None

async def insert_new_session(
        conn: asyncpg.Connection,
        user_id: str
):
    session_id = await conn.fetchval(
    """INSERT INTO sessions (user_id) 
    values ($1) RETURNING session_id
    """,user_id
    ) 
    return str(session_id)
async def insert_refresh_token(
    conn: asyncpg.Connection,
    session_id: str,
    hashed_refresh_token: str
):
    result =await conn.fetchval(
    """UPDATE sessions SET hashed_refresh_token 
    = $2 WHERE session_id = $1 RETURNING session_id
    """,session_id,hashed_refresh_token
    )
    return str(result) if result else None
async def logout_session(conn: asyncpg.Connection,session_id: str):
    await conn.execute("""UPDATE sessions SET IS_ACTIVE = false WHERE 
        session_id = $1 """,session_id)
    