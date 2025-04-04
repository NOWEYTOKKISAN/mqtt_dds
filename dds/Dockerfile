FROM python:3.10

WORKDIR /app

# 필수 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 및 데이터 파일 복사
COPY ddsPub.py .
COPY ddsSub.py .
COPY industrial_robot_control_6G_network.csv .

CMD ["python3", "ddsPub.py"]
