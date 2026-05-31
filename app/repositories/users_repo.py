import asyncpg

from uuid import UUID

async def get_user_by_email(conn: asyncpg.Connection,email: str):
    user = await conn.fetchrow(
        """SELECT email,username,sign_up_type
         FROM users WHERE email = $1""",
         email
    )
    return dict(user)
