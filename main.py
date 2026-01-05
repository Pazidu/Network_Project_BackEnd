from fastapi import FastAPI
from database import engine
from models import Base
from auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"status": "Backend running"}
