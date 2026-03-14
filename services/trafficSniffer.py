import scapy.all as scapy
import threading
from datetime import datetime
from services.deviceServices import device_cache, cache_lock
from scapy.layers.dns import DNS, DNSQR
from models.Sitevisited import WebsiteLog
from services.websiteService import save_dns
from wifi_info import get_wifi_info  
from scapy.layers.inet import IP
from scapy.layers.dns import DNS, DNSQR
# from scapy.all import sniff 



def packet_handler(packet):
    if not packet.haslayer(scapy.Ether) or not packet.haslayer(scapy.IP):
        return

    size = len(packet)
    now = datetime.utcnow().isoformat() + "Z"

    src_ip = packet[scapy.IP].src
    dst_ip = packet[scapy.IP].dst
    src_mac = packet[scapy.Ether].src.lower()
    dst_mac = packet[scapy.Ether].dst.lower()

    protocol = "OTHER"
    src_port = dst_port = None

    if packet.haslayer(scapy.TCP):
        protocol = "TCP"
        src_port = packet[scapy.TCP].sport
        dst_port = packet[scapy.TCP].dport
    elif packet.haslayer(scapy.UDP):
        protocol = "UDP"
        src_port = packet[scapy.UDP].sport
        dst_port = packet[scapy.UDP].dport

    session_id = f"{src_ip}:{src_port}→{dst_ip}:{dst_port}/{protocol}"
    # # -------- DNS Detection --------
    # if packet.haslayer(DNS) and packet.haslayer(DNSQR):
    #     dns_query = packet[DNSQR].qname.decode().rstrip(".")
    
    # # only log real domain names (avoid local junk)
    # if "." in dns_query:
    #     wifi_id = get_wifi_info()
    #     save_dns(src_mac, dns_query, wifi_id=1)  

    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
        dns = packet[DNS]

    if dns.qr == 0:
        domain = packet[DNSQR].qname.decode().rstrip(".").lower()
        source_mac = packet[scapy.Ether].src.lower()

        if "." not in domain:
            return

        IGNORE = ["gstatic", "connectivitycheck", "windows"]

        if any(x in domain for x in IGNORE):
            return

        print(f"{source_mac} visited {domain}")

        save_dns(source_mac, domain)

    with cache_lock:
        src_key = f"{src_ip}_{src_mac}"
        dst_key = f"{dst_ip}_{dst_mac}"

        # -------- SOURCE DEVICE --------
        if src_key in device_cache:
            dev = device_cache[src_key]

            dev["bytes_sent"] += size
            dev["packets_sent"] += 1

            sessions = dev["sessions"]
            if session_id not in sessions:
                sessions[session_id] = {
                    "protocol": protocol,
                    "src": f"{src_ip}:{src_port}",
                    "dst": f"{dst_ip}:{dst_port}",
                    "start_time": now,
                    "last_seen": now,
                    "bytes": size,
                    "packets": 1
                }
            else:
                s = sessions[session_id]
                s["last_seen"] = now
                s["bytes"] += size
                s["packets"] += 1

        # -------- DEST DEVICE --------
        if dst_key in device_cache:
            dev = device_cache[dst_key]
            dev["bytes_recv"] += size
            dev["packets_recv"] += 1

# sniff(filter="udp port 53", prn=packet_handler)
def start_sniffer(interface=None):
    print(f"Sniffer started on interface: {interface}")
    scapy.sniff(
        iface=interface,
        filter="udp port 53",
        prn=packet_handler,
        store=False,
        promisc=True
    )


def start_traffic_sniffer(interface=None):
    threading.Thread(
        target=start_sniffer,
        kwargs={"interface": interface},
        daemon=True
    ).start()
