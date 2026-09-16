from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.db.database import Base , engine
from app.db import models
#根据 models.py 里的表结构创建数据库表。
Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(products_router, prefix="/api/products")

@app.get("/health")
def root():
    return {"status": "ok"}
