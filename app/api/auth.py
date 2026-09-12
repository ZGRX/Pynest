from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegisterRequest, UserLoginRequest,UserResponse

router = APIRouter()

users = []

@router.post("/register",response_model = UserResponse)
def register(data: UserRegisterRequest):
    for user in users:
        if user["email"] == data.email:
            raise HTTPException(status_code = 400,detail="Email already registered")
        
    user = {
        "id":len(users) + 1,
        "username":data.username,
        "email":data.email,
        "password":data.password,
    }
    users.append(user)
    return {
        "id":user["id"],
        "username": user["username"],
        "email":user["email"],
    }

@router.post("/login")
def login(data: UserLoginRequest):
    for user in users:
        if user["email"] == data.email and user["password"] == data.password:
            return {
                "message": "login success",
                "user":{
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"]
                }
            }

    raise HTTPException(status_code=400, detail="Invalid email or password")
