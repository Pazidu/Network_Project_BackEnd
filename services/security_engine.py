from datetime import datetime

def calculate_risk(device, is_new=False, high_usage=False, frequent_disconnect=False):
    score = 0

    # 1️⃣ New Device
    if is_new:
        score += 30

    # 2️⃣ High Usage
    if high_usage:
        score += 25

    # 3️⃣ Frequent Disconnect
    if frequent_disconnect:
        score += 20

    # 4️⃣ Unknown Device Name
    if device.device_name == "Unknown":
        score += 15

    # Limit to 100
    score = min(score, 100)

    # Decide Risk Level
    if score >= 70:
        level = "Dangerous"
    elif score >= 40:
        level = "Warning"
    else:
        level = "Safe"

    return score, level