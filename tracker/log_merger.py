# placeholder
import json
import os

IGNORED_PROCESSES = {
    "System Idle Process", "System", "svchost.exe", "RuntimeBroker.exe",
    "winlogon.exe", "sihost.exe", "csrss.exe", "explorer.exe",
    "SearchIndexer.exe", "ctfmon.exe", "taskhostw.exe", "SecurityHealthService.exe"
}

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def clean_app_name(name):
    if not name or name in IGNORED_PROCESSES:
        return None

    if "Visual Studio Code" in name:
        return "Visual Studio Code"
    if "Brave" in name:
        return "Brave"
    if "WhatsApp" in name:
        return "WhatsApp"
    if "PC Tracker" in name:
        return "PC Tracker"
    if "Task Switching" in name:
        return "Task Switching"
    if "Snipping Tool" in name:
        return "Snipping Tool"

    return name.strip()

def merge_logs(focused_log_path, background_log_path):
    focused = load_json(focused_log_path)
    background = load_json(background_log_path)

    combined = {}

    for app, secs in focused.get("apps", {}).items():
        clean_name = clean_app_name(app)
        if clean_name is None:
            continue
        combined[clean_name] = combined.get(clean_name, 0) + secs

    for app, details in background.items():
        clean_name = clean_app_name(app)
        if clean_name is None:
            continue
        combined[clean_name] = combined.get(clean_name, 0) + details.get("total_minutes", 0) * 60

    sorted_combined = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return [(name, int(secs)) for name, secs in sorted_combined[:5]]
