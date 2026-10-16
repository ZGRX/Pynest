from datetime import datetime
from pydantic import BaseModel,Field
# 专门放商品相关的 API 数据格式
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(ge=0)
    stock: int = Field(default=0,ge=0)

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
    price: float | None = Field(default=None , ge=0)
    stock: int | None = Field(default=None,ge = 0)
    is_active: bool |None = None
    created_at: datetime | None = None