from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socket
import scapy.all as scapy

from routes.userRoutes import router as user_router

app = FastAPI()

# CORS for mobile frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Utility: Get local IP address
# -----------------------------
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# -----------------------------
# Network Scan Logic
# -----------------------------
def scan_network():
    local_ip = get_local_ip()
    subnet = local_ip.rsplit(".", 1)[0] + ".0/24"

    arp = scapy.ARP(pdst=subnet)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = scapy.srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for _, received in result:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc,
            "status": "online"
        })

    return devices

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/devices")
def get_devices():
    return {
        "count": len(scan_network()),
        "devices": scan_network()
    }

# User routes
app.include_router(user_router, prefix="/user")
