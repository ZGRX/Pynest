from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserRegisterRequest, UserLoginRequest,UserResponse
from app.db.database import get_db
from app.db.models import User

router = APIRouter()

users = []

@router.post("/register",response_model = UserResponse)
def register(data:UserRegisterRequest, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username = data.username,
        email = data.email,
        password = data.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login")
def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if user.password != data.password:
        raise HTTPException(status_code=400,detail="Invalid email or password")

    return {
        "message": "login success",
        "user":{
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }
