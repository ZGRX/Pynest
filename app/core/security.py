from passlib.context import CryptContext
from datetime import datetime , timedelta , timezone
from jose import jwt
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
ACCESS_TOEKN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password:str):
    return pwd_context.verify(password,hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOEKN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})#用来添加或更新键值。

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt