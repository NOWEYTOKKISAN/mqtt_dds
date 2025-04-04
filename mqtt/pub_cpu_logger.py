import time
import csv
import psutil
import os

print("[pub-cpu] Starting CPU logging...")

log_path = "/app/pub_cpu.csv"
with open(log_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_percent"])
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            timestamp = time.time()
            writer.writerow([timestamp, cpu])
            print(f"[pub-cpu] {timestamp:.2f}, {cpu:.2f}%")
            f.flush()
    except KeyboardInterrupt:
        print("[pub-cpu] Logging stopped.")
