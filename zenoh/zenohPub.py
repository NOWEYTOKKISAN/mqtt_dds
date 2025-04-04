import time
import json
import csv
import psutil
from settingParams import MSG_SIZE, PUB_INTERVAL, ZENOH_TOPIC

from zenoh import open
from zenoh.config import Config

# CSV 파일 초기화
with open("/app/pub_log.csv", mode="w", newline="") as log_file:
    writer = csv.writer(log_file)
    writer.writerow(["timestamp", "message"])

with open("/app/pub_cpu.csv", mode="w", newline="") as cpu_file:
    cpu_writer = csv.writer(cpu_file)
    cpu_writer.writerow(["timestamp", "cpu_percent"])

    # Zenoh 설정 및 세션 생성
    conf = config.Config()
    session = open(conf)
    pub = session.declare_publisher(ZENOH_TOPIC)

    try:
        while True:
            timestamp = time.time()
            payload = json.dumps({"timestamp": timestamp, "payload": "x" * MSG_SIZE})
            pub.put(payload)

            # 로그 기록
            with open("/app/pub_log.csv", mode="a", newline="") as log_file:
                writer = csv.writer(log_file)
                writer.writerow([timestamp, payload])

            # CPU 사용률 기록
            cpu = psutil.cpu_percent(interval=None)
            cpu_writer.writerow([timestamp, cpu])
            cpu_file.flush()

            time.sleep(PUB_INTERVAL)
    except KeyboardInterrupt:
        pass
