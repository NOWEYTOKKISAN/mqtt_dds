# 실험 세팅값 수정
# 전송 주기 (초)
PUB_INTERVAL = 0.1  # 10Hz

# 메시지 크기 (bytes)
MSG_SIZE = 1024  # 1KB

# 전송 토픽/키
ZENOH_TOPIC = "demo/perf"

# 로깅 경로
PUB_LOG = "pub_log.csv"
SUB_LOG = "sub_log.csv"
PUB_CPU_LOG = "pub_cpu.csv"
SUB_CPU_LOG = "sub_cpu.csv"
