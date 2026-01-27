import psutil
import socket
import subprocess
import platform
import re

def get_wifi_info():
    """Get detailed Wi-Fi info on Windows using netsh (Updated for Signal Health & DNS)"""
    info = {}
    try:
        
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"], 
            capture_output=True, text=True, errors="ignore"
        )
        output = result.stdout
        
    
        def get_val(pattern):
            match = re.search(pattern, output)
            return match.group(1).strip() if match else None

        
        info['ssid'] = get_val(r"SSID\s*:\s*(.*)")
        info['bssid'] = get_val(r"BSSID\s*:\s*(.*)")
        info['adapter_name'] = get_val(r"Name\s*:\s*(.*)")
        
        
        info['signal_quality'] = get_val(r"Signal\s*:\s*(\d+)%") 
        
        
        info['channel'] = get_val(r"Channel\s*:\s*(\d+)")
        info['rx_rate'] = get_val(r"Receive rate \(Mbps\)\s*:\s*([\d\.]+)")
        info['tx_rate'] = get_val(r"Transmit rate \(Mbps\)\s*:\s*([\d\.]+)")
        info['radio_type'] = get_val(r"Radio type\s*:\s*(.*)")
        info['band'] = get_val(r"Band\s*:\s*(.*)") or "Unknown"

        
        if info['band'] == "Unknown" and info['radio_type']:
            rt = info['radio_type'].lower()
            if "ac" in rt or "ax" in rt: info['band'] = "5 GHz"
            elif "n" in rt: info['band'] = "2.4 / 5 GHz"
            elif "g" in rt or "b" in rt: info['band'] = "2.4 GHz"

        
        if info['adapter_name']:
            ip_result = subprocess.run(
                ["netsh", "interface", "ip", "show", "config", info['adapter_name']], 
                capture_output=True, text=True, errors="ignore"
            )
            ip_output = ip_result.stdout

            
            #info['ipv4_address'] = re.search(r"IP Address\s*:\s*([\d\.]+)", ip_output).group(1) if re.search(r"IP Address\s*:\s*([\d\.]+)", ip_output) else "Unknown"
            info['gateway'] = re.search(r"Default Gateway\s*:\s*([\d\.]+)", ip_output).group(1) if re.search(r"Default Gateway\s*:\s*([\d\.]+)", ip_output) else "Unknown"

            
            dns_match = re.search(r"DNS servers.*:\s*([\d\.\s]+)", ip_output, re.MULTILINE)
            if dns_match:
                raw_dns = dns_match.group(1)
                
                info['dns_servers'] = [x.strip() for x in raw_dns.split() if x.strip()]
            else:
                info['dns_servers'] = ["Unknown"]

    except Exception as e:
        print(f"Error extracting Wi-Fi info: {e}")
        info['error'] = str(e)
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
        wifi_info = get_wifi_info()
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
