import asyncpg

async def search_users(conn: asyncpg.Connection,search_users: str,current_user: str) :
    users = await conn.fetch(
        """SELECT id , username FROM users WHERE username ILIKE $1
        AND id != $2 LIMIT 20""",f"%{search_users}%",current_user
    )
    if users:
        return [
    {
        "id": str(user["id"]),
        "username": user["username"]
    }
    for user in users
]
    return None
