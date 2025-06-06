# -!- coding: utf-8 -!-
import torch
import torchvision.models as models
import redis
from pickle import dumps, loads
from efficientnet_b7_split import SecondNet

model = models.efficientnet_b7()
model.eval()
children = [
    list(child.children()) if list(child.children()) else [child]
    for child in list(model.children())
]

avgpool = children[1][0]
print(avgpool)
classifier = children[2][0]
print(classifier)
children = [item for sublist in children[0] for item in sublist]
delay_list = []
r = redis.StrictRedis(host="localhost", port=6379, db=1)
r1 = redis.StrictRedis(host="localhost", port=6379, db=0)

for split_layer in range(3, 57):
    second_model = SecondNet(children, split_layer, avgpool, classifier)
    second_model.eval()
    second_model.to("cpu")
    this_random = 1
    for i in range(100):
        a = r.get("yolov5backbone_A1_{}".format(this_random))
        while a == None:
            a = r.get("yolov5backbone_A1_{}".format(this_random))
            continue
        r0 = loads(a)
        tensor_r = second_model(r0[0])
        r.delete("yolov5backbone_A1_{}".format(this_random))
        this_random = r0[1]
    print("Beginning identifying the second part")
    r1.set("preheat", "OK")
    for i in range(250):
        a = r.get("yolov5backbone_A1_{}".format(this_random))
        while a == None:
            a = r.get("yolov5backbone_A1_{}".format(this_random))
            continue
        r0 = loads(a)
        tensor_r = second_model(r0[0])
        r.delete("yolov5backbone_A1_{}".format(this_random))
        this_random = r0[1]
    print("Split {} layer, finish the second part identification".format(split_layer))
    r1.set("Flag", "OK")
