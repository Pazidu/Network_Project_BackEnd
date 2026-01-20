import psutil
import socket
import subprocess
import platform

def get_windows_wifi_info():
    """Get Wi-Fi info on Windows using netsh"""
    info = {}
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("SSID") and "BSSID" not in line:
                info['ssid'] = line.split(":", 1)[1].strip()
            elif line.startswith("Signal"):
                info['signal_strength'] = line.split(":", 1)[1].strip()
            elif line.startswith("BSSID"):
                info['mac'] = line.split(":", 1)[1].strip()
            elif line.startswith("Name"):
                info['adapter_name'] = line.split(":", 1)[1].strip()
    except:
        pass
    return info

def get_ip_mac_info(interface):
    """Get IP and MAC using psutil"""
    ip = None
    mac = None
    addrs = psutil.net_if_addrs().get(interface, [])
    for addr in addrs:
        if addr.family == socket.AF_INET:
            ip = addr.address
        if addr.family == psutil.AF_LINK:
            mac = addr.address
    return ip, mac

def get_network_info():
    system = platform.system()
    
    if system == "Windows":
        wifi_info = get_windows_wifi_info()
        interface = wifi_info.get("adapter_name")
        ip, mac = get_ip_mac_info(interface) if interface else (None, None)
        
        # gateway and DNS on Windows via psutil
        gateways = psutil.net_if_stats()
        gateway = None  # Optional: can use netifaces for full info
        dns = []  # Optional: use win32api or netsh command
        
    else:  # Linux
        from pyroute2 import IPRoute
        iproute = IPRoute()
        # default interface
        interface = None
        for route in iproute.get_default_routes(family=socket.AF_INET):
            oif = route.get('oif')
            if oif:
                interface = iproute.get_links(oif)[0].get_attr('IFLA_IFNAME')
                break
        
        ip, mac = get_ip_mac_info(interface) if interface else (None, None)
        dns = []
        try:
            with open("/etc/resolv.conf") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        dns.append(line.split()[1])
        except:
            pass
        
        gateway = None
        for route in iproute.get_default_routes(family=socket.AF_INET):
            gw = route.get_attr('RTA_GATEWAY')
            if gw:
                gateway = gw
                break
        
        wifi_info = {
            "adapter_name": interface,
            "ssid": None,
            "signal_strength": None,
            "mac": mac
        }
    
    # Stats
    stats = psutil.net_io_counters(pernic=True).get(interface, {}) if interface else {}

    result = {
        "interface": interface,
        "ip": ip,
        "gateway": gateway,
        "dns": dns,
        "stats": {
            "bytes_sent": stats.bytes_sent if stats else None,
            "bytes_recv": stats.bytes_recv if stats else None,
            "packets_sent": stats.packets_sent if stats else None,
            "packets_recv": stats.packets_recv if stats else None
        },
        "status": "connected" if ip else "disconnected",
        **wifi_info
    }

    return result

# Example usage
if __name__ == "__main__":
    info = get_network_info()
    print(info)
