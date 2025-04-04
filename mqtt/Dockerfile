# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 주요 파일 복사
COPY mqttPub_from_csv.py /app/mqttPub_from_csv.py
COPY mqttSub.py /app/mqttSub.py
COPY pub_cpu_logger.py /app/pub_cpu_logger.py
COPY sub_cpu_logger.py /app/sub_cpu_logger.py
COPY IOT-temp.csv /app/IOT-temp.csv
COPY industrial_robot_control_6G_network.csv /app/industrial_robot_control_6G_network.csv

RUN pip install paho-mqtt psutil

CMD ["bash"]
