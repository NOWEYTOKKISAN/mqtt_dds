import csv
import time
import psutil
from cyclonedds.idl import IdlStruct
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import Subscriber, DataReader

class Message(IdlStruct):
    robot_id: str
    task_type: str
    timestamp: str
    data_size: int
    data_transfer_time: float
    latency: float
    packet_loss_rate: float
    resource_allocation: float

participant = DomainParticipant()
subscriber = Subscriber(participant)
topic = Topic(participant, "Industrial_Robot_Data", Message)
reader = DataReader(subscriber, topic)

print("📡 Subscriber is receiving messages...")

output_file = "received_data.csv"
cpu_log_file = "sub_cpu.csv"
sub_log_file = "sub_log.csv"

with open(cpu_log_file, mode="w", newline="") as cpu_file, \
     open(output_file, mode="w", newline="") as file, \
     open(sub_log_file, mode="w", newline="") as sub_log:

    cpu_writer = csv.writer(cpu_file)
    writer = csv.writer(file)
    sub_writer = csv.writer(sub_log)

    cpu_writer.writerow(["timestamp", "cpu_percent"])
    writer.writerow(["timestamp", "resource_allocation", "packet_loss_rate", "latency", "data_size", "data_transfer_time"])
    sub_writer.writerow(["received_timestamp", "sent_timestamp", "latency"])

    while True:
        samples = reader.take()
        if samples:
            for msg in samples:
                recv_ts = time.time()
                if msg.timestamp:
                    try:
                        sent_ts = float(msg.timestamp)
                        latency = recv_ts - sent_ts
                    except ValueError:
                        latency = -1.0
                        print(f"⚠️ Could not convert timestamp: {msg.timestamp}")
                else:
                    latency = -1.0
                    print("⚠️ Empty timestamp!")

                writer.writerow([
                    msg.timestamp,
                    msg.resource_allocation,
                    msg.packet_loss_rate,
                    msg.latency,
                    msg.data_size,
                    msg.data_transfer_time
                ])

                sub_writer.writerow([recv_ts, msg.timestamp, latency])
                sub_log.flush()

                print(f"✅ Received: {msg.timestamp} (Latency: {latency:.4f} s)")
        else:
            print("⏳ No new data...")

        cpu_percent = psutil.cpu_percent(interval=0.1)
        timestamp = time.time()
        cpu_writer.writerow([timestamp, cpu_percent])
        cpu_file.flush()
        time.sleep(1)
