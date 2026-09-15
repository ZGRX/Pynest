from passlib.context import CryptContext
from datetime import datetime , timedelta , timezone
from jose import jwt
from jose import JWSError
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

def decode_access_token(token:str) -> dir | None:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWSError:
        return None
        # encode 时：algorithm=ALGORITHM
        # decode 时：algorithms=[ALGORITHM]
