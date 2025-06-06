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

fig, ax = plt.subplots(1, 3, figsize=(8, 3))
fig.suptitle("Each Throughput vs Split Point")
fig.supxlabel("Split Point")

ax[0].plot(x, y1)
ax[0].set_ylabel("Total Throughput")

ax[1].plot(x, y2)
ax[1].set_ylabel("First Throughput")

ax[2].plot(x, y3)
ax[2].set_ylabel("Second Throughput")

plt.tight_layout()

plt.show()
