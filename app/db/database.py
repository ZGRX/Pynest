from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./pynest.db"#SQLite 数据库文件地址。

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
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