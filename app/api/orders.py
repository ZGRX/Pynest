from fastapi import APIRouter, HTTPException,Depends
from app.db.database import get_db
from app.db.models import Product,Order
from app.schemas.order import OrderCreate,OrderResponse
from app.api.auth import get_current_user
from sqlalchemy.orm import Session
from app.core.constants import ORDER_STATUS_CANCELLED,ORDER_STATUS_PENDING,ORDER_STATUS_PAID

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

@router.get("/",response_model=list[OrderResponse])
def list_my_orders(
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)#花括号里的：{order_id}，表示这是一个路径参数。
def get_order(
    order_id: int,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404,detail="Order not found")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to access this order")

    return order

@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to cancel this order")

    if order.status != ORDER_STATUS_PENDING:
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")

    product = db.query(Product).filter(Product.id == order.product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product.stock += order.quantity
    order.status = ORDER_STATUS_CANCELLED

    db.commit()
    db.refresh(order)

    return order

@router.post("/{order_id}/pay", response_model=OrderResponse)
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to pay this order")

    if order.status != ORDER_STATUS_PENDING:
        raise HTTPException(status_code=400, detail="Only pending orders can be paid")

    order.status = ORDER_STATUS_PAID

    db.commit()
    db.refresh(order)

    return order        
#pending     待支付 / 待处理
#paid        已支付
#shipped     已发货
#completed   已完成
#cancelled   已取消        