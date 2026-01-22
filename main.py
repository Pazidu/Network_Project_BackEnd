from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.userRoutes import router as user_router

from routes.pingRoutes import ping_router 

from routes.deviceRoutes import router as device_router
from routes.wifi import router as wifi_router
from services.deviceServices import start_scanner

from core.database import engine
from models import * 
from core.database import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


# CORS for mobile frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"status": "Backend running"}
app.include_router(user_router, prefix="/user")
app.include_router(ping_router, prefix="/ping")
app.include_router(device_router, prefix="/devices")
app.include_router(wifi_router, prefix="/network")

@app.on_event("startup")
def startup_event():
    start_scanner()