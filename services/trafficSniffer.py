import scapy.all as scapy
import threading
from services.deviceServices import device_cache, cache_lock

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
                    dev["bytes_sent"] += size
                    dev["packets_sent"] += 1
                elif dev["ip"] == dst_ip:
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
