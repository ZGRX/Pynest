from datetime import datetime
from pydantic import BaseModel
#用户需要传什么。
class OrderCreate(BaseModel):
    product_id:int 
    quantity:int

class OrderResponse(BaseModel):
    id:int 
    user_id:int
    product_id:int
    quantity:int
    total_price:float
    status:str
    created_at:datetime