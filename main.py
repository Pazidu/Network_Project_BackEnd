from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scapy.all import get_if_list, get_if_addr

from routes.userRoutes import router as user_router
from routes.pingRoutes import ping_router
from routes.deviceRoutes import router as device_router
from routes.wifi import router as wifi_router

from services.deviceServices import start_scanner
from services.trafficSniffer import start_traffic_sniffer

from core.database import engine
from models import *
from core.database import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


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
app.include_router(device_router)
app.include_router(wifi_router, prefix="/network")


@app.on_event("startup")
def startup_event():
    print("Starting ARP scanner...")
    start_scanner()

 
    interfaces = get_if_list()
    local_iface = None
    for iface in interfaces:
        ip = get_if_addr(iface)
        if ip != "127.0.0.1":
            local_iface = iface
            break

    if local_iface:
        print(f"Starting traffic sniffer on interface: {local_iface}")
        start_traffic_sniffer(interface=local_iface)
    else:
        print("No valid network interface found. Traffic sniffer not started.")
