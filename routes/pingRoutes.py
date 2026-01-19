from fastapi import APIRouter
from ping3 import ping

ping_router = APIRouter()

@ping_router.get("")
def ping_host():
    latency = ping("8.8.8.8", timeout=1)
    if latency is None:
        return {"ping": None}
    return {"ping": int(latency * 1000)}
