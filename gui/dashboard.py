# placeholder
import customtkinter as ctk
from tracker.uptime_tracker import get_system_uptime
from tracker.activity_tracker import IdleMonitor
from tracker.log_merger import merge_logs
from tracker.window_tracker import AppUsageTracker
from tracker.visualizer import plot_app_usage

from datetime import datetime
import os
import json

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PC Tracker")
        self.geometry("400x320")

        self.idle_monitor = IdleMonitor()
        self.app_tracker = AppUsageTracker()

        self.uptime_label = ctk.CTkLabel(self, text="Uptime: Calculating...")
        self.uptime_label.pack(pady=10)

        self.idle_label = ctk.CTkLabel(self, text="Idle Time: Calculating...")
        self.idle_label.pack(pady=10)

        self.top_apps_label = ctk.CTkLabel(self, text="Top Apps:\nLoading...")
        self.top_apps_label.pack(pady=10)

        self.graph_button = ctk.CTkButton(self, text="Show Graph", command=self.show_graph)
        self.graph_button.pack(pady=10)

        self.update_labels()
        self.mainloop()

    def update_labels(self):
        uptime = get_system_uptime()
        idle_time = self.idle_monitor.get_idle_duration()

        self.uptime_label.configure(text=f"Uptime: {str(uptime).split('.')[0]}")
        self.idle_label.configure(text=f"Idle: {int(idle_time)} seconds")

        today = datetime.now().date()
        focused_path = os.path.join("logs", f"{today}.json")
        background_path = os.path.join("logs", f"bg_apps_{today}.json")
        top_apps = merge_logs(focused_path, background_path)

        top_apps_text = "Top Apps:\n"
        for name, secs in top_apps:
            mins = secs // 60
            top_apps_text += f"{name[:25]} - {mins} min\n"

        self.top_apps_label.configure(text=top_apps_text)
        self.after(5000, self.update_labels)

    def show_graph(self):
        today = datetime.now().date()
        focused_path = os.path.join("logs", f"{today}.json")
        background_path = os.path.join("logs", f"bg_apps_{today}.json")
        combined = {}

        if os.path.exists(focused_path):
            with open(focused_path) as f:
                focused = json.load(f).get("apps", {})
                for k, v in focused.items():
                    combined[k] = combined.get(k, 0) + v

        if os.path.exists(background_path):
            with open(background_path) as f:
                bg = json.load(f)
                for k, v in bg.items():
                    combined[k] = combined.get(k, 0) + v.get("total_minutes", 0) * 60

        plot_app_usage(combined)
