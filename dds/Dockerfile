FROM python:3.10

WORKDIR /dds

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ddsPub.py .
COPY ddsSub.py .
COPY cpu_plot.py .
COPY industrial_robot_control_6G_network.csv .

CMD ["python3", "ddsPub.py"]
