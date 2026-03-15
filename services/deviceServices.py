import socket
import scapy.all as scapy
import threading
import time
from datetime import datetime
from services.oui import OUI_MAP
from services.deviceHistoryService import update_device_uptime
from wifi_info import get_wifi_info
from services.wifiUtils import get_current_wifi

device_cache = {}
cache_lock = threading.Lock()

SCAN_INTERVAL = 30
OFFLINE_AFTER = 60

# ------------------ Helpers ------------------

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def get_manufacturer(mac: str) -> str:
    return OUI_MAP.get(mac.upper()[0:8], "Unknown")


def resolve_device_name(ip, mac):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        if hostname and hostname != ip:
            return hostname
    except Exception:
        pass

    manufacturer = get_manufacturer(mac)
    if manufacturer != "Unknown":
        return f"{manufacturer} ({mac[-5:]})"

    return f"Device ({mac[-5:]})"

# ------------------ Scanner ------------------

def perform_scan():
    print(socket.gethostbyname(socket.gethostname()))
    ssid, bssid = get_current_wifi()

    if not ssid or not bssid:
        print("Wi-Fi info not available")
        return

    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return

    subnet = local_ip.rsplit(".", 1)[0] + ".0/24"

    arp = scapy.ARP(pdst=subnet)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    wifi =get_wifi_info()
    interface = wifi.get("adapter_name")

    if not interface:
        print("No WIFI interface found for scanning")
        return
    try:
        result = scapy.srp(
                            packet,
                            timeout=3,
                            iface=interface,   # or specify WiFi adapter name
                            verbose=False
                        )[0]

    except PermissionError:
        print("Run as Administrator")
        return

    now = datetime.utcnow()
    seen = set()

    with cache_lock:
        for _, received in result:
            dev_id = f"{received.psrc}_{received.hwsrc.lower()}"
            seen.add(dev_id)

            device_name = resolve_device_name(received.psrc, received.hwsrc)

            if dev_id not in device_cache:
                device_cache[dev_id] = {
                    "id": dev_id,
                    "ip": received.psrc,
                    "mac": received.hwsrc.lower(),
                    "manufacturer": get_manufacturer(received.hwsrc),
                    "device_name": device_name,
                    "status": "online",
                    "connected_at": now.isoformat() + "Z",
                    "last_seen": now.isoformat() + "Z",
                    "disconnected_at": None,
                    "bytes_sent": 0,
                    "bytes_recv": 0,
                    "packets_sent": 0,
                    "packets_recv": 0,
                    "sessions": {}
                }
            else:
                dev = device_cache[dev_id]
                dev["status"] = "online"
                dev["last_seen"] = now.isoformat() + "Z"
                dev["disconnected_at"] = None

            update_device_uptime(
                ip=received.psrc,
                mac=received.hwsrc.lower(),
                name=device_name,
                ssid=ssid,
                bssid=bssid
            )


        for dev in device_cache.values():
            last_seen = datetime.fromisoformat(dev["last_seen"].replace("Z", ""))
            if (now - last_seen).total_seconds() > OFFLINE_AFTER:
                if dev["status"] == "online":
                    dev["status"] = "offline"
                    dev["disconnected_at"] = now.isoformat() + "Z"

            

    print("Local IP:", local_ip)
    print("Subnet:", subnet)
    print("ARP Raw Result:", result)
    print("ARP Count:", len(result))


    print(f"Scan complete: {len(seen)} devices online")

   
   




def scan_loop():
    while True:
        perform_scan()
        time.sleep(SCAN_INTERVAL)


def start_scanner():
    threading.Thread(target=scan_loop, daemon=True).start()


def get_cached_devices():
    with cache_lock:
        return list(device_cache.values())



def force_scan():
    perform_scan()

