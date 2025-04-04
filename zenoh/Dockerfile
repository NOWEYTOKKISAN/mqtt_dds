FROM python:3.10-slim

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

WORKDIR /app

# Rust 설치를 위한 환경 준비
RUN apt-get update && \
    apt-get install -y git curl build-essential && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y --profile minimal
# 환경변수 설정
ENV PATH="/root/.cargo/bin:${PATH}"

# 파일 복사
COPY *.py /app/
COPY settingParams.py /app/

# 의존성 설치
RUN pip install psutil pandas matplotlib && \
    pip install git+https://github.com/eclipse-zenoh/zenoh-python.git

CMD ["bash"]
