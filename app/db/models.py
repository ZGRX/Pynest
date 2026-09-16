from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    #index=True 是 给这一列加索引

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,primary_key=True,nullable=False)
    description = Column(String,nullable=True)
    price = Column(Integer,nullable=False)
    stock = Column(Integer,nullable=False,default=0)
    is_active = Column(Boolean,nullable=False,default=True)
    created_at = Column(DateTime,default=lambda: datetime.now(timezone.utc))