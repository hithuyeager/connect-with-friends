import asyncpg

async def search_users(conn: asyncpg.Connection,search_users: str,current_user: str) :
    users = await conn.fetch(
        """SELECT id , username FROM users WHERE username ILIKE $1
        AND id != $2 LIMIT 20""",search_users,current_user
    )
    return dict(users) if users else None
