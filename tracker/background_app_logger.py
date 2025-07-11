import psutil
import time
import json
import os
from datetime import datetime

class BackgroundAppLogger:
    def __init__(self):
        self.app_sessions = {}
        self.interval = 30
        self.logs_dir = "logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        self.current_log_date = datetime.now().date()
        self.log_file = self.get_log_file_path()

    def get_log_file_path(self):
        return os.path.join(self.logs_dir, f"bg_apps_{self.current_log_date}.json")

    def scan_processes(self):
        current_time = time.time()
        running_apps = set()

        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name']
                if name:
                    running_apps.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        for name in running_apps:
            if name not in self.app_sessions:
                self.app_sessions[name] = {
                    "start_time": current_time,
                    "last_seen": current_time,
                    "total_duration": 0
                }
            else:
                self.app_sessions[name]["last_seen"] = current_time
                self.app_sessions[name]["total_duration"] += self.interval

        to_delete = []
        for name, info in self.app_sessions.items():
            if name not in running_apps and current_time - info["last_seen"] > 300:
                to_delete.append(name)
        for name in to_delete:
            del self.app_sessions[name]

    def save_log(self):
        data_to_save = {
            name: {
                "start_time": datetime.fromtimestamp(info["start_time"]).strftime("%H:%M:%S"),
                "last_seen": datetime.fromtimestamp(info["last_seen"]).strftime("%H:%M:%S"),
                "total_minutes": int(info["total_duration"] // 60)
            } for name, info in self.app_sessions.items()
        }

        with open(self.log_file, "w") as f:
            json.dump(data_to_save, f, indent=2)

    def run(self):
        try:
            while True:
                today = datetime.now().date()
                if today != self.current_log_date:
                    self.save_log()
                    self.app_sessions.clear()
                    self.current_log_date = today
                    self.log_file = self.get_log_file_path()

                self.scan_processes()
                self.save_log()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.save_log()
