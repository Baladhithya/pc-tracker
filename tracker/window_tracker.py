# placeholder
import time
import os
import json
from datetime import datetime
try:
    import win32gui
except ImportError:
    win32gui = None

class AppUsageTracker:
    def __init__(self):
        self.usage_data = {}  # {app_name: total_seconds}
        self.last_app = None
        self.last_switch_time = time.time()
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)

    def get_active_window(self):
        if win32gui:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        return "Unknown"

    def update_usage(self):
        current_app = self.get_active_window()
        now = time.time()
        if self.last_app:
            duration = now - self.last_switch_time
            self.usage_data[self.last_app] = self.usage_data.get(self.last_app, 0) + duration

        self.last_app = current_app
        self.last_switch_time = now

    def save_usage_to_file(self):
        today = datetime.now().date()
        log_path = os.path.join(self.log_dir, f"{today}.json")
        with open(log_path, "w") as f:
            json.dump({"apps": {k: int(v) for k, v in self.usage_data.items()}}, f, indent=2)
