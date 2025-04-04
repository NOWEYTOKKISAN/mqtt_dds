# DDS-MQTT-ZENOH

## [결과 확인]

무조건 새로 빌드되게 하려면 캐시 없이 빌드해야:

docker-compose down --volumes --remove-orphans
docker-compose build --no-cache
docker-compose up

특히 --no-cache를 꼭 써야 Docker가 pub_cpu_logger.py를 인식한다

실행 : docker-compose up --build

[시각화]
아래 명령어를 터미널에 입력
docker cp mqtt-pub-csv:/app/pub_log.csv ./pub_log.csv 
docker cp mqtt-sub:/app/sub_log.csv ./sub_log.csv 
docker cp pub-cpu:/app/pub_cpu.csv ./pub_cpu.csv 
docker cp sub-cpu:/app/sub_cpu.csv ./sub_cpu.csv

아래 명령어 실행으로 손실률 확인
python3 calculate_loss.py

cd..으로 상위 폴더로 이동 후
아래 명령어 실행으로 시각화 진행
# 사용예시
# python3 visualize_results.py --source mqtt
# python3 visualize_results.py --source dds
