from pydantic import BaseModel

class DirectRoomSchema(BaseModel):
    target_user_id: str