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
