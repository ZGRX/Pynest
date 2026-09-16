from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/",response_model=ProductResponse)
def create_product(
    data:ProductCreate,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = Product(
        name = data.name,
        description = data.description,
        price = data.price,
        stock = data.stock,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return product
