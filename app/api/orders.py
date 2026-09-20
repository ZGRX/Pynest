from fastapi import APIRouter, HTTPException,Depends
from app.db.database import get_db
from app.db.models import Product,Order
from app.schemas.order import OrderCreate,OrderResponse
from app.api.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()
@router.post("/",response_model=OrderResponse)
def create_order(
    data:OrderCreate,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    if not product.is_active:
        raise HTTPException(status_code=400,detail="Product is not active")
    if product.stock<data.quantity:
        raise HTTPException(status_code=400,detail="Product is empty")
    
    order = Order(
        user_id = current_user.id,
        product_id = product.id,
        quantity = data.quantity,
        total_price = product.price * data.quantity,
    )

    product.stock -= data.quantity

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

