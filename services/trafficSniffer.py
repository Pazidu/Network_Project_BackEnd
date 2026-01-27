import scapy.all as scapy
import threading
from services.deviceServices import device_cache, cache_lock

def packet_handler(packet):
    if not packet.haslayer(scapy.Ether):
        return

    src_mac = packet[scapy.Ether].src.lower()
    dst_mac = packet[scapy.Ether].dst.lower()
    size = len(packet)

    # Compose keys as "ip_mac" strings by looking up IPs from packets (if possible)
    src_ip = packet[scapy.IP].src if packet.haslayer(scapy.IP) else None
    dst_ip = packet[scapy.IP].dst if packet.haslayer(scapy.IP) else None

    with cache_lock:
        # Match src device in cache by ip_mac key
        if src_ip and src_mac:
            src_key = f"{src_ip}_{src_mac}"
            if src_key in device_cache:
                device_cache[src_key]["bytes_sent"] += size
                device_cache[src_key]["packets_sent"] += 1
                # print(f"Updated sent for {src_key}")

        # Match dst device in cache by ip_mac key
        if dst_ip and dst_mac:
            dst_key = f"{dst_ip}_{dst_mac}"
            if dst_key in device_cache:
                device_cache[dst_key]["bytes_recv"] += size
                device_cache[dst_key]["packets_recv"] += 1
                # print(f"Updated recv for {dst_key}")



    # print(packet.summary())
    # print("PACKET", src_mac, dst_mac, size)


    # except Exception as e:
    #     print("Packet handler error:", e)


def start_sniffer(interface=None):
    print(f"Sniffer started on interface: {interface}")
    scapy.sniff(
        iface=interface,
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
