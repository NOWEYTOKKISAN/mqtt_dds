# calculate_loss.py
import csv
import os

PUB_LOG = "pub_log.csv"
SUB_LOG = "sub_log.csv"
OUT_PATH = "log/loss_result.csv"

def load_ids(path):
    ids = set()
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ids.add(int(row["id"]))
            except:
                continue
    return ids

pub_ids = load_ids(PUB_LOG)
sub_ids = load_ids(SUB_LOG)

total_sent = len(pub_ids)
total_recv = len(sub_ids)
loss = total_sent - total_recv
loss_rate = (loss / total_sent) * 100 if total_sent > 0 else 0

print(f"전송 수: {total_sent}, 수신 수: {total_recv}, 손실 수: {loss}, 손실률: {loss_rate:.2f}%")

os.makedirs("log", exist_ok=True)
with open(OUT_PATH, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["total_sent", "total_received", "loss_count", "loss_rate(%)"])
    writer.writerow([total_sent, total_recv, loss, round(loss_rate, 2)])
