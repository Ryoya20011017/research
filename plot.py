import csv
import matplotlib.pyplot as plt

# データ読み込み
x = []  # split_point
y1 = []  # total_throughput
y2 = []  # first_throughput
y3 = []  # second_throughput

# ファイル名を入力してもらう
file_name = input("CSVファイル名を入力してください（例：data.csv）: ")


with open(str(file_name), newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        x.append(int(row["split_point"]))
        y1.append(float(row["total_throughput"]))
        y2.append(float(row["first_throughput"]))
        y3.append(float(row["second_throughput"]))

# グラフ描画
plt.plot(x, y1, label="Total Throughput")
plt.plot(x, y2, label="First Throughput")
plt.plot(x, y3, label="Second Throughput")

plt.xlabel("Split Point")
plt.ylabel("Throughput")
plt.title("Throughput vs Split Point")
plt.legend()
plt.grid(True)

plt.xlim(left=0)  # ← x軸の下限を0に固定
plt.xlim(right=60)  # ← x軸の上限を60に固定

plt.tight_layout()
plt.show()
