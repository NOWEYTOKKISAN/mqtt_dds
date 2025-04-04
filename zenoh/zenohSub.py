import time
import json
import csv
from settingParams import ZENOH_TOPIC

from zenoh import open
from zenoh.config import Config

# CSV 파일 초기화
with open("/app/sub_log.csv", mode="w", newline="") as log_file:
    writer = csv.writer(log_file)
    writer.writerow(["timestamp", "latency_ms"])

# Zenoh 설정 및 세션 생성
conf = config.Config()
session = open(conf)

# 서브스크라이버 선언
def callback(sample):
    now = time.time()
    data = json.loads(sample.payload.decode())
    latency = (now - data["timestamp"]) * 1000  # ms

    # 로그 기록
    with open("/app/sub_log.csv", mode="a", newline="") as log_file:
        writer = csv.writer(log_file)
        writer.writerow([now, latency])

session.declare_subscriber(ZENOH_TOPIC, callback)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
