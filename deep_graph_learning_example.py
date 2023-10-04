import os

os.environ["DGLBACKEND"] = "pytorch"
import dgl
import dgl.data
import torch
import torch.nn as nn
import torch.nn.functional as F

dataset = dgl.data.CoraGraphDataset()
print(f"Number of categories: {dataset.num_classes}")