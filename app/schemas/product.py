from datetime import datetime
from pydantic import BaseModel
# 专门放商品相关的 API 数据格式
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int = 0

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    is_active: bool
    created_at: datetime

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    is_active: bool |None = None
    created_at: datetime | None = None