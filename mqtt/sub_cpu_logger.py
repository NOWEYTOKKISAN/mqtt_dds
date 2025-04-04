import psutil
import time
import csv

log_path = "/app/sub_cpu.csv"  # 꼭 /app 경로로 설정
with open(log_path, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_percent"])

    while True:
        cpu = psutil.cpu_percent(interval=1)
        writer.writerow([time.time(), cpu])
        f.flush()