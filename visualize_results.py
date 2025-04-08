import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os

# -------------------------------
# 사용예시
# python3 visualize_results.py --source mqtt
# python3 visualize_results.py --source dds
# -------------------------------

# -------------------------------
# CLI 인자 설정
# -------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, required=True, choices=["mqtt", "dds"], help="Data source to visualize")
args = parser.parse_args()

base_path = os.path.join(os.getcwd(), args.source)

# -------------------------------
# 1. Latency 시각화
# -------------------------------
#df = pd.read_csv(os.path.join(base_path, "sub_log.csv"))
#plt.figure()
#plt.plot(df["timestamp"].to_numpy(), df["latency_ms"].to_numpy())
#plt.title(f"[{args.source.upper()}] Latency Over Time")
#plt.xlabel("Time")
#plt.ylabel("Latency (ms)")
#plt.grid()
#plt.savefig(f"{args.source}_latency.png")

# -------------------------------
# 2. Throughput 시각화
# -------------------------------
#df["time_sec"] = df["timestamp"].astype(int)
#throughput = df.groupby("time_sec").size()
#plt.figure()
#throughput.plot()
#plt.title(f"[{args.source.upper()}] Throughput (msg/sec)")
#plt.xlabel("Time (s)")
#plt.ylabel("Messages")
#plt.grid()
#plt.savefig(f"{args.source}_throughput.png")

# -------------------------------
# 3. CPU 사용률 시각화
# -------------------------------
pub_cpu_path = os.path.join(base_path, "pub_cpu.csv")
sub_cpu_path = os.path.join(base_path, "sub_cpu.csv")

if os.path.exists(pub_cpu_path) and os.path.exists(sub_cpu_path):
    pub_cpu = pd.read_csv(pub_cpu_path)
    sub_cpu = pd.read_csv(sub_cpu_path)

    plt.figure()
    plt.plot(pub_cpu["timestamp"].to_numpy(), pub_cpu["cpu_percent"].to_numpy(), label="Publisher")
    plt.plot(sub_cpu["timestamp"].to_numpy(), sub_cpu["cpu_percent"].to_numpy(), label="Subscriber")
    plt.title(f"[{args.source.upper()}] CPU Usage Over Time")
    plt.xlabel("Time")
    plt.ylabel("CPU %")
    plt.legend()
    plt.grid()
    plt.savefig(f"{args.source}_cpu_usage.png")

plt.show()
