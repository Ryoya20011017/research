import os
import csv

values = [1, 2, 3]
base_name = "data"
ext = ".csv"
filename = base_name + ext
i = 1

# 同名ファイルが存在する限り、新しいファイル名を生成する
while os.path.exists(filename):
    filename = f"{base_name}_{i}{ext}"
    i += 1

# ファイルに書き込み
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "split_point",
            "total_throughput",
            "total_elapsed_time",
            "first_throughput",
            "first_elapsed_time",
            "second_throughput",
            "second_elapsed_time"
        ]
    )

    data=[]
    for i in range(5,30):
        data.append((i, 1/30, 30,i,1/i,30-i,1/(30-i)))
    writer.writerows(data)
print(f"Saved as: {filename}")
