values = [1,2,3]
with open("hoge.txt", "w") as o:
    print(*values, sep="\n",file = o)
