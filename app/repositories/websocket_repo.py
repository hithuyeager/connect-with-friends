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

async def add_messages(
    conn:asyncpg.Connection,
    room_id: str,
    sender_id: str,
    message: str
):
    await conn.execute(
        """INSERT INTO messages (room_id,sender_id,message) 
        values ($1,$2,$3)
        """,room_id,sender_id,message
    )

async def get_messages(
    conn: asyncpg.Connection,
    room_id: str,
    offset: int,
    limit: int
):
    messages = await conn.fetch(
        """
        SELECT sender_id,message,sent_at 
        FROM messages WHERE room_id = $1 
        ORDER BY sent_at DESC
        OFFSET $2 LIMIT $3
        """,room_id,offset,limit
    )
    if messages:
        return [
            {
                "sender_id" : str(message["sender_id"]),
                "message" : message["message"],
                "sent_at" : message["sent_at"].isoformat()
            }
            for message in messages
        ] 
    else:
        return None

