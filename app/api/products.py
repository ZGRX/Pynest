from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Product
from app.schemas.product import ProductCreate, ProductResponse,ProductUpdate
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

@router.get("/",response_model=list[ProductResponse])
def list_products(db:Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/{product_id}",response_model = ProductResponse)
def get_products(product_id:int,db:Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    return product

@router.put("/{product_id}",response_model=ProductResponse)
def update_product(
    product_id: int ,
    data: ProductUpdate,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)#setattr() 是 Python 内置函数，用来动态设置对象属性。

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{product.id}",response_model=ProductResponse)
def delete_product(
    product_id:int ,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404,detail="Product not found")

    product.is_active = False
    db.commit()
    db.refresh(product)

    return product