import socket
import scapy.all as scapy
import threading
import time

device_cache = []
cache_lock = threading.Lock()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def perform_scan():
    global device_cache

    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        print("No valid local IP found")
        return

    subnet = f"{local_ip}/24"

    arp = scapy.ARP(pdst=subnet)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    try:
        result = scapy.srp(packet, timeout=2, verbose=False)[0]
    except PermissionError:
        print("ERROR: Run server as root/admin (Scapy needs it)")
        return

    new_devices = []

    for _, received in result:
        new_devices.append({
            "id": f"{received.psrc}_{received.hwsrc}",
            "ip": received.psrc,
            "mac": received.hwsrc,
            "status": "online"
        })

    with cache_lock:
        device_cache = new_devices

    print(f"Scan complete: {len(device_cache)} devices found")


def scan_loop():
    while True:
        perform_scan()
        time.sleep(30)   # scan every 30 seconds


def start_scanner():
    thread = threading.Thread(target=scan_loop, daemon=True)
    thread.start()


def get_cached_devices():
    with cache_lock:
        return device_cache
