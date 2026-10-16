from fastapi import APIRouter, HTTPException,Depends
from app.api.auth import get_current_user,get_current_admin_user
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models import User,Product,Order
from sqlalchemy import func
from app.core.constants import ORDER_STATUS_PAID,ORDER_STATUS_CANCELLED,ORDER_STATUS_PENDING
router = APIRouter()

@router.get("/dashboard")
def get_dashboard(
    db:Session = Depends(get_db),
    current_user = Depends(get_current_admin_user),
):  
    paid_number = db.query(Order).filter(Order.status == ORDER_STATUS_PAID).count()
    cancelled_number = db.query(Order).filter(Order.status == ORDER_STATUS_CANCELLED).count()
    pending_number = db.query(Order).filter(Order.status == ORDER_STATUS_PENDING).count()
    product = db.query(Product).count()
    order = db.query(Order).count()
    user = db.query(User).count()
    paid_revenue = (
        db.query(func.sum(Order.total_price))
        .filter(Order.status == ORDER_STATUS_PAID)
        .scalar()
        or 0
    )

    dashboard = {
        "user" : user,
        "order" : order,
        "product" : product,
        "paid_number": paid_number,
        "cancelled_number":cancelled_number,
        "pending_number":pending_number,
        "paid_revenue":paid_revenue
    }
    return dashboard
