import asyncpg

from uuid import UUID

async def get_user_by_email(conn: asyncpg.Connection,email: str):
    user = await conn.fetchrow(
        """SELECT email,username,sign_up_type
         FROM users WHERE email = $1""",
         email
    )
    return dict(user)

async def add_app_user(
    conn: asyncpg.Connection,
    email: str,
    username: UUID,
    password: str,
    sign_up_type: str = "app login"
):
    await conn.execute(
        """ INSERT INTO  users 
        (email,username,password,sign_up_type) 
        values ($1,$2,$3,$4)""",
        email,username,password,sign_up_type)
    
