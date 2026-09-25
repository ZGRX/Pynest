from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    username:str
    email: str
    password:str


class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin:bool

class TokenResponse(BaseModel):
    access_token:str
    token_type: str
    