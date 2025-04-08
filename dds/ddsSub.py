import time
import psutil
import csv
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import Subscriber, DataReader
from cyclonedds.idl import IdlStruct

LOG_FILE = "sub_cpu.csv"

class Message(IdlStruct):
    robot_id: str
    task_type: str
    task_duration: float
    energy_consumption: float
    position_coordinates: str
    robot_speed: float
    sensor_id: str
    sensor_type: str
    sensor_reading: float
    timestamp: str
    data_size: int
    network_load: float
    network_latency: float
    packet_loss_rate: float
    network_type: str
    slice_id: str
    slice_bandwidth: int
    command_delay: float
    feedback_delay: float
    data_transfer_time: float
    total_delay: float
    signal_strength: float
    latency: float
    resource_allocation: float
    error_rate: float

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)

# 로그 파일 초기화
with open(LOG_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "cpu_percent"])

print("✅ DDS Subscriber 시작됨...")

# DDS 설정
participant = DomainParticipant()
subscriber = Subscriber(participant)
topic = Topic(participant, "Industrial_Robot_Data", Message)
reader = DataReader(subscriber, topic)

try:
    while True:
        samples = reader.take()
        if not samples:
            print("⏳ No new data...")
        for data in samples:
            if data:
                print(f"📥 수신 데이터: {data.robot_id}, {data.task_type}, {data.timestamp}")

        # CPU 사용률 측정 후 로그 저장
        cpu_percent = psutil.cpu_percent(interval=0.1)
        timestamp = time.time()
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, cpu_percent])

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 수신 중단됨")
