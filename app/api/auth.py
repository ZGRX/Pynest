from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserRegisterRequest, UserLoginRequest,UserResponse,TokenResponse
from app.db.database import get_db
from app.db.models import User
from app.core.security import get_password_hash , verify_password,create_access_token,decode_access_token
from fastapi.security import OAuth2PasswordBearer
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")###？？？

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db:Session = Depends(get_db),
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401,detail="Invalid authentication token")
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

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

@router.get("/me",response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user