import socket
import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ping3 import ping

ping_router = APIRouter()

@ping_router.get("/")
def ping_host():
    start = time.time()
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        latency = int((time.time() - start) * 1000)
        return {"status": "up", "ping": latency}
    except:
        return {"status": "down", "ping": None}
