import csv
import time
import psutil
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.pub import Publisher, DataWriter
from cyclonedds.idl import IdlStruct

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

participant = DomainParticipant()
topic = Topic(participant, "Industrial_Robot_Data", Message)  
publisher = Publisher(participant)
writer = DataWriter(publisher, topic)

csv_filename = "industrial_robot_control_6G_network.csv"
cpu_log_file = "pub_cpu.csv"

with open(cpu_log_file, mode="w", newline="") as cpu_file:
    cpu_writer = csv.writer(cpu_file)
    cpu_writer.writerow(["timestamp", "cpu_percent"])

    with open(csv_filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            msg = Message()
            msg.robot_id = row["robot_id"]
            msg.task_type = row["task_type"]
            msg.task_duration = float(row["task_duration"])
            msg.energy_consumption = float(row["energy_consumption"])
            msg.position_coordinates = row["position_coordinates"]
            msg.robot_speed = float(row["robot_speed"])
            msg.sensor_id = row["sensor_id"]
            msg.sensor_type = row["sensor_type"]
            msg.sensor_reading = float(row["sensor_reading"])
            msg.timestamp = row["timestamp"]
            msg.data_size = int(row["data_size"])
            msg.network_load = float(row["network_load"])
            msg.network_latency = float(row["network_latency"])
            msg.packet_loss_rate = float(row["packet_loss_rate"])
            msg.network_type = row["network_type"]
            msg.slice_id = row["slice_id"]
            msg.slice_bandwidth = int(row["slice_bandwidth"])
            msg.command_delay = float(row["command_delay"])
            msg.feedback_delay = float(row["feedback_delay"])
            msg.data_transfer_time = float(row["data_transfer_time"])
            msg.total_delay = float(row["total_delay"])
            msg.signal_strength = float(row["signal_strength"])
            msg.latency = float(row["latency"])
            msg.resource_allocation = float(row["resource_allocation"])
            msg.error_rate = float(row["error_rate"])

            writer.write(msg)
            print(f"📤 Sent data: {msg.robot_id}, {msg.task_type}, {msg.timestamp}")

            cpu_percent = psutil.cpu_percent(interval=0.1)
            timestamp = time.time()
            cpu_writer.writerow([timestamp, cpu_percent])
            cpu_file.flush()
            time.sleep(0.1)

print("✅ Finished publishing. Waiting before exit...")
time.sleep(3)
