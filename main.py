from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.userRoutes import router as user_router
from routes.deviceRoutes import router as device_router

app = FastAPI()

# CORS for mobile frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running"}

app.include_router(user_router, prefix="/user")
app.include_router(device_router, prefix="/devices")
