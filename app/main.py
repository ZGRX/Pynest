from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.db.database import Base , engine
from app.db import models

Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")


@app.get("/health")
def root():
    return {"status": "ok"}
