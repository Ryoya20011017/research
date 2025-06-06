# -!- coding: utf-8 -!-
import torch
import torchvision.models as models
import redis
import random
import time
from pickle import dumps
from efficientnet_b7_split import FirstNet
import multiprocessing as mp
from multiprocessing import Queue, Process

model = models.efficientnet_b7()
model.eval()
children = [
    list(child.children()) if list(child.children()) else [child]
    for child in list(model.children())
]

children = [item for sublist in children[0] for item in sublist]

delay_list = []
data = []
for i in range(350):
    img = torch.randn(1, 3, 224, 224).to("cpu")
    data.append(img)

# r = redis.StrictRedis(host='192.168.163.124', port=6379, db=0)
r = redis.StrictRedis(host="localhost", port=6379, db=1)
# r = redis.StrictRedis(host='10.240.59.242', port=6379, db=0)
r1 = redis.StrictRedis(host="localhost", port=6379, db=0)


class detect:
    def __init__(self, sl):
        self.split_layer = sl
        self.first_model = FirstNet(children, self.split_layer)
        self.first_model.eval()
        self.first_model.to("cpu")
        self.DATA_redis = [None, None]

    def detect_first(self, i, i1, i2, q):
        r = self.first_model(data[i])
        self.DATA_redis[0] = r
        self.DATA_redis[1] = i2
        b = dumps(self.DATA_redis)
        q.put(b)
        q.put(i1)


def save(qc):
    q = qc
    for itt in range(350):
        b = q.get()
        i = q.get()
        r.set("yolov5backbone_A1_{}".format(i), b)
    print("Identification of the first part finished")


def dete(wq, d_queue, sl):
    split_layer = sl
    i1 = 1
    q = d_queue
    q1 = wq
    f = detect(sl)
    print("warm up......")
    for i in range(100):
        i2 = random.uniform(2, 100)
        f.detect_first(i, i1, i2, q)
        i1 = i2
    while r1.get("preheat") == None:
        continue
    r1.delete("preheat")
    print("Start identification of the first part")
    t1 = time.perf_counter()
    for i in range(100, 350):
        i2 = random.uniform(2, 100)
        f.detect_first(i, i1, i2, q)
        i1 = i2

    t1_1 = time.perf_counter()

    while r1.get("Flag") == None:
        continue
    r1.delete("Flag")
    t2 = time.perf_counter()
    first_t = t1_1-t1
    second_t = t2-t1_1
    t = t2 - t1
    print("Split {} layer，time consumption is {}s, first {}s, second {}s".format(split_layer, t, first_t, second_t))
    q1.put((t, first_t, second_t))


if __name__ == "__main__":
    print("hello")
    mp.set_start_method("spawn")

    for split_layer in range(3, 5):
        q = Queue()
        wq = Queue()
        detect_A1 = Process(target=dete, args=(wq, q, split_layer))
        detect_A1.start()
        save(q)
        detect_A1.join()
        a = wq.get()
        delay_list.append(a)
        wq.close()
    i = 40
    for item in delay_list:
        t, first_t, second_t = item
        print(i, f"Total: {t:.3f}s, First: {first_t:.3f}s, Second: {second_t:.3f}s\n")
        #print(i, item, "\n")
        i = i + 1
