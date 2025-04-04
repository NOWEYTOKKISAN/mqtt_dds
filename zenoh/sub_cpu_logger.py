# sub_cpu_logger.py
import psutil
import time
import csv

with open("/app/sub_cpu.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_percent"])

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            writer.writerow([time.time(), cpu])
            f.flush()
    except KeyboardInterrupt:
        pass
