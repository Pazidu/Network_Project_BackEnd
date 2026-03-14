import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scapy.all import get_if_list, get_if_addr
import uvicorn
from routes.userRoutes import router as user_router
from routes.pingRoutes import ping_router
from routes.deviceRoutes import router as device_router
from routes.wifi import router as wifi_router
from routes.networkUsageRoutes import usage_router
from services.deviceServices import start_scanner
from services.trafficSniffer import start_traffic_sniffer
from routes.deviceHistoryRoute import router as device_history_route
from wifi_info import get_wifi_info  # import get_wifi_info to get adapter name
from routes.notificationRoute import router as notification_router
from routes.secrity_summeryRoute import router as security_summary_route

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
app.include_router(device_router, prefix="/devices")
app.include_router(wifi_router, prefix="/network")
app.include_router(device_history_route)
app.include_router(usage_router, prefix="/network-usage")
app.include_router(notification_router)
app.include_router(security_summary_route)



@app.on_event("startup")
def startup_event():
    print("Starting ARP scanner...")
    start_scanner()

    wifi = get_wifi_info()
    iface = wifi.get("adapter_name")

    if iface:
        print(f"Starting traffic sniffer on Wi-Fi interface: {iface}")
        start_traffic_sniffer(interface=iface)
    else:
        print("Wi-Fi adapter not found. Traffic sniffer not started.")

# def start_backend():
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)

# # Start the backend in a background thread
# threading.Thread(target=start_backend, daemon=True).start()
