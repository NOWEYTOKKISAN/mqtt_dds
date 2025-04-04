import cyclonedds
from cyclonedds.idl import IdlStruct
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import Subscriber, DataReader

# 메시지 구조체 정의
class Message(IdlStruct):
    robot_id: str
    task_type: str
    timestamp: str  # 원래 datetime이면 변환 필요

# 도메인 생성
participant = DomainParticipant()

# 구독자(Subscriber) 생성
subscriber = Subscriber(participant)

# 토픽 생성
topic = Topic(participant, "RobotControlTopic", Message)

# 데이터 리더 생성
reader = DataReader(subscriber, topic)

print("📡 Subscriber is ready to receive messages...")

# 데이터 수신 루프
while True:
    try:
        samples = reader.take()
        for msg in samples:
            print(f"📩 Received data: {msg.robot_id}, {msg.task_type}, {msg.timestamp}")
    except Exception as e:
        print(f"❌ Error reading data: {e}")
