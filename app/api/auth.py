from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserRegisterRequest, UserLoginRequest,UserResponse,TokenResponse
from app.db.database import get_db
from app.db.models import User
from app.core.security import get_password_hash , verify_password,create_access_token

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
        password = get_password_hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login",response_model=TokenResponse)
def login(data: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(data.password,user.password):
        raise HTTPException(status_code=400,detail="Invalid email or password")

    access_token = create_access_token(data={"sub":user.email})
    #sub 是 JWT 常用字段，意思是：subject，这个 token 属于谁
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
