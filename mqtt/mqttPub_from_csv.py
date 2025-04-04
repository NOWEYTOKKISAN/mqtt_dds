# mqttPub_from_csv.py
import time, json, csv
import paho.mqtt.client as mqtt
import os

CSV_PATH = "/app/industrial_robot_control_6G_network.csv"
LOG_PATH = "/app/pub_log.csv"
MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883
MQTT_TOPIC = "test/latency"
PUBLISH_INTERVAL = 0.1

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()
msg_id = 0

def generate_fixed_size_payload(row, target_size_bytes=512):
    # 최소 구성
    base_msg = {
        "id": 0,
        "timestamp": time.time(),
        "data": row
    }

    base_str = json.dumps(base_msg)
    base_size = len(base_str.encode())

    # 필요한 padding 계산
    padding_bytes = max(0, target_size_bytes - base_size)
    row["padding"] = "X" * padding_bytes

    return row

# 로그 디렉토리 보장
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# 로그 파일 열기
with open(LOG_PATH, "w", newline='') as logfile:
    log_writer = csv.writer(logfile)
    log_writer.writerow(["id", "timestamp", "payload"])

    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            now = time.time()
            fixed_data = generate_fixed_size_payload(row, target_size_bytes=1024)
            msg = {
                "id": msg_id,
                "timestamp": now,
                "data": fixed_data
            }
            payload = json.dumps(msg)
            client.publish(MQTT_TOPIC, payload)
            actual_size = len(payload.encode())
    
            print(f"[mqttPub_from_csv] Published: {msg}, Payload size: {actual_size} bytes")

            log_writer.writerow([msg_id, now, payload]) 
            msg_id += 1                               

            time.sleep(PUBLISH_INTERVAL)

print("[mqttPub_from_csv] Finished publishing.")
