from datetime import datetime
import os
import json
import requests
import atexit
import psutil

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ✅ Used in GUI to calculate system uptime
def get_system_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    return datetime.now() - boot_time

def get_log_path():
    today = datetime.now().date()
    return os.path.join(LOG_DIR, f"{today}.json")

# 🕒 Log system boot time + location
def log_boot_time():
    path = get_log_path()
    data = {}
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)

    data["date"] = str(datetime.now().date())
    data["boot_time"] = datetime.now().strftime("%H:%M:%S")

    # 🌍 Add location if not already present
    if "location" not in data:
        try:
            loc = requests.get("https://ipinfo.io/json").json()
            data["location"] = {
                "city": loc.get("city", "Unknown"),
                "region": loc.get("region", "Unknown"),
                "country": loc.get("country", "Unknown"),
                "loc": loc.get("loc", "")
            }
        except:
            data["location"] = {
                "city": "N/A",
                "region": "N/A",
                "country": "N/A",
                "loc": ""
            }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# 📴 Log logout time on exit
def log_logout_time():
    path = get_log_path()
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        data["logout_time"] = datetime.now().strftime("%H:%M:%S")
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

# Automatically log logout on program exit
atexit.register(log_logout_time)
