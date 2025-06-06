import torch
import torch.nn as nn
class FirstNet(nn.Module):
    def __init__(self , children, split_layer):
        super(FirstNet, self).__init__()
        self.first_layer = nn.Sequential(*children[:split_layer])

    def forward(self, x):
        x = self.first_layer(x)
        return x


class SecondNet(nn.Module):
    def __init__(self , children, split_layer,avgpool,classifier):
        super(SecondNet, self).__init__()
        self.second_layer = nn.Sequential(*children[split_layer:58])
        self.avgpool = avgpool
        self.classifier = classifier

    def forward(self, x):
        x = self.second_layer(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
