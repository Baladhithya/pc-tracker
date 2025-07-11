# placeholder
from gui.dashboard import Dashboard
from tracker.background_app_logger import BackgroundAppLogger
from tracker.window_tracker import AppUsageTracker
from tracker.uptime_tracker import log_boot_time
import threading
import time


def run_focused_tracker(tracker):
    while True:
        try:
            tracker.update_usage()
            tracker.save_usage_to_file()
        except Exception as e:
            print("Foreground tracker error:", e)
        time.sleep(2)


if __name__ == "__main__":
    log_boot_time()
    threading.Thread(target=BackgroundAppLogger().run, daemon=True).start()
    threading.Thread(target=run_focused_tracker, args=(AppUsageTracker(),), daemon=True).start()
    Dashboard()
