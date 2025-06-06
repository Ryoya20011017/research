import os

values = [1, 2, 3]
base_name = "hoge"
ext = ".txt"
filename = base_name + ext
i = 1

# 同名ファイルが存在する限り、新しいファイル名を生成する
while os.path.exists(filename):
    filename = f"{base_name}_{i}{ext}"
    i += 1

# ファイルに書き込み
with open(filename, "w") as o:
    print(*values, sep="\n", file=o)

print(f"Saved as: {filename}")