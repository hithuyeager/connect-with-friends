from pydantic import BaseModel,EmailStr,Field

class Signup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    username: str = Field(min_length=8,max_length=12)

class Signin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
class RefreshToken(BaseModel):
    refresh_token: str