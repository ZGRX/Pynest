from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#数据库类型驱动 用户名：密码 地址：端口
DATABASE_URL = "postgresql+psycopg://postgres:pynest_dev@127.0.0.1:5433/pynest"
engine = create_engine(
    DATABASE_URL,
)
#用来创建数据库 session。
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()