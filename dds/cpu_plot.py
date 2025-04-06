import matplotlib.pyplot as plt
import pandas as pd

# 데이터 로드
pub_df = pd.read_csv("pub_cpu.csv")
sub_df = pd.read_csv("sub_cpu.csv")

plt.figure(figsize=(10, 6))

# 그래프 출력
plt.plot(pub_df["timestamp"], pub_df["cpu_percent"], label="Publisher", linewidth=1)
plt.plot(sub_df["timestamp"], sub_df["cpu_percent"], label="Subscriber", linewidth=1)

plt.xlabel("Time")
plt.ylabel("CPU %")
plt.title("📊 CPU Usage Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
