import socket
import scapy.all as scapy
import threading
import time
from datetime import datetime
from services.oui import OUI_MAP
from services.deviceHistoryService import update_device_uptime
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


def get_hostname(ip: str):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def resolve_device_name(ip, mac):
    hostname = get_hostname(ip)
    if hostname:
        return hostname
    manufacturer = get_manufacturer(mac)
    return f"{manufacturer} device"

# ------------------ Packet Tracking ------------------

def packet_handler(packet):
    try:
        if not packet.haslayer(scapy.IP):
            return
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        size = len(packet)

        with cache_lock:
            for dev in device_cache.values():
                if dev["ip"] == src_ip:
                    dev.setdefault("bytes_sent", 0)
                    dev.setdefault("packets_sent", 0)
                    dev["bytes_sent"] += size
                    dev["packets_sent"] += 1
                elif dev["ip"] == dst_ip:
                    dev.setdefault("bytes_recv", 0)
                    dev.setdefault("packets_recv", 0)
                    dev["bytes_recv"] += size
                    dev["packets_recv"] += 1
    except Exception as e:
        print("Packet handler error:", e)


def start_sniffer(interface=None):
    scapy.sniff(
        iface=interface,
        prn=packet_handler,
        store=False
    )


def start_traffic_sniffer(interface=None):
    threading.Thread(
        target=start_sniffer,
        kwargs={"interface": interface},
        daemon=True
    ).start()

# ------------------ Scanner ------------------

def perform_scan():
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return

    subnet = local_ip.rsplit(".", 1)[0] + ".0/24"

    arp = scapy.ARP(pdst=subnet)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    try:
        result = scapy.srp(packet, timeout=2, verbose=False)[0]
    except PermissionError:
        print("Run as Administrator")
        return

    now = datetime.utcnow()
    seen = set()

    with cache_lock:
        for _, received in result:
            dev_id = f"{received.psrc}_{received.hwsrc}"
            seen.add(dev_id)

            device_name = resolve_device_name(received.psrc, received.hwsrc)

            if dev_id not in device_cache:
                device_cache[dev_id] = {
                    "id": dev_id,
                    "ip": received.psrc,
                    "mac": received.hwsrc,
                    "manufacturer": get_manufacturer(received.hwsrc),
                    "device_name": device_name,
                    "status": "online",
                    "connected_at": now.isoformat() + "Z",
                    "last_seen": now.isoformat() + "Z",
                    "disconnected_at": None,
                    "bytes_sent": 0,
                    "bytes_recv": 0,
                    "packets_sent": 0,
                    "packets_recv": 0
                }
            else:
                dev = device_cache[dev_id]
                dev["status"] = "online"
                dev["last_seen"] = now.isoformat() + "Z"
                dev["disconnected_at"] = None

            # ✅ MOVE THIS INSIDE THE LOOP
            update_device_uptime(
                ip=received.psrc,
                mac=received.hwsrc,
                name=device_name
            )

    print(f"Scan complete: {len(seen)} devices online")


def scan_loop():
    while True:
        perform_scan()
        time.sleep(SCAN_INTERVAL)


def start_scanner():
    threading.Thread(target=scan_loop, daemon=True).start()


def force_scan():
    perform_scan()


def get_cached_devices():
    with cache_lock:
        return list(device_cache.values())
