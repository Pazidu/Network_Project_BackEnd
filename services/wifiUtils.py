import subprocess

def get_current_wifi():
    try:
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"],
            encoding="utf-8",
            errors="ignore"
        )

        ssid = None
        bssid = None

        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[1].strip()
            elif "BSSID" in line:
                bssid = line.split(":", 1)[1].strip()

        return ssid, bssid
    except Exception:
        return None, None
