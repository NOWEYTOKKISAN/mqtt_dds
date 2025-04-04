import time, json, csv
import paho.mqtt.client as mqtt
import os

# === 설정 ===
PUB_LOG_PATH = "/app/pub_log.csv"         # 퍼블리셔 로그 (Docker 내부 경로 기준)
SUB_LOG_PATH = "/app/sub_log.csv"         # 수신 로그 저장 위치
LOSS_LOG_PATH = "/app/loss_result.csv"    # 손실률 기록 파일

# === 변수 초기화 ===
count = 0
total_latency = 0
received = 0
received_ids = set()

# === 수신 로그 파일 준비 ===
os.makedirs("/app", exist_ok=True)
csv_file = open(SUB_LOG_PATH, "w", newline="")
writer = csv.writer(csv_file)
writer.writerow(["id", "timestamp", "latency_ms"])

def on_message(client, userdata, msg):
    global count, total_latency, received
    print("[mqtt-sub] Message received!")

    received += 1
    try:
        raw = json.loads(msg.payload.decode())
        msg_id = raw.get("id")

        if msg_id is not None:
            received_ids.add(int(msg_id))

        if "timestamp" in raw:
            latency = (time.time() - raw["timestamp"]) * 1000
            print(f"[mqtt-sub] Latency: {latency:.2f} ms")

            total_latency += latency
            count += 1
            writer.writerow([msg_id, time.time(), round(latency, 3)])
            csv_file.flush()
        else:
            print("[mqtt-sub] No timestamp found.")
    except Exception as e:
        print("[mqtt-sub] Decode error:", e)

def calculate_loss():
    try:
        with open(PUB_LOG_PATH, newline='') as f:
            reader = csv.DictReader(f)
            pub_ids = set()
            for row in reader:
                try:
                    pub_ids.add(int(row["id"]))
                except:
                    continue

        total_sent = len(pub_ids)
        total_recv = len(received_ids)
        loss_count = total_sent - total_recv
        loss_rate = (loss_count / total_sent) * 100 if total_sent > 0 else 0

        print(f"[mqtt-sub] 총 전송: {total_sent}, 수신: {total_recv}, 손실: {loss_count}, 손실률: {loss_rate:.2f}%")

        with open(LOSS_LOG_PATH, "w", newline='') as logf:
            log_writer = csv.writer(logf)
            log_writer.writerow(["total_sent", "total_received", "loss_count", "loss_rate(%)"])
            log_writer.writerow([total_sent, total_recv, loss_count, round(loss_rate, 2)])
    except FileNotFoundError:
        print(f"[mqtt-sub] 퍼블리셔 로그 파일이 존재하지 않습니다: {PUB_LOG_PATH}")

# === MQTT 연결 ===
client = mqtt.Client()
client.connect("mqtt-broker", 1883)
client.subscribe("test/latency")
client.on_message = on_message

# === 실행 ===
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("[mqtt-sub] Stopping subscriber...")
finally:
    csv_file.close()
    calculate_loss()
