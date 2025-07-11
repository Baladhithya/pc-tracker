# placeholder
import matplotlib.pyplot as plt

def plot_app_usage(app_usage):
    labels = list(app_usage.keys())
    times = [t // 60 for t in app_usage.values()]
    plt.figure(figsize=(8, 5))
    plt.barh(labels, times, color='skyblue')
    plt.xlabel("Minutes")
    plt.title("App Usage Time")
    plt.tight_layout()
    plt.show()
