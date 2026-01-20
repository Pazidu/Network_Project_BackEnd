import socket
import time
from fastapi import APIRouter

ping_router = APIRouter(prefix="/ping")

@ping_router.get("/")
def ping_host():
    start = time.time()
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        latency = int((time.time() - start) * 1000)
        return {"status": "up", "ping": latency}
    except:
        return {"status": "down", "ping": None}
