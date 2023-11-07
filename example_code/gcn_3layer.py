import dgl
import torch
import torch.nn.functional as F
import torch.nn as nn
from dgl.nn import GraphConv


class GCN3L(nn.Module):
    """Example 2 layer GCN"""

    def __init__(self, in_feats: int, h1_feats: int, h2_feats: int, num_classes: int):
        super(GCN3L, self).__init__()
        self.conv1 = GraphConv(in_feats, h1_feats)
        self.conv2 = GraphConv(h1_feats, h2_feats)
        self.conv3 = GraphConv(h2_feats, num_classes)

    def forward(self, g: dgl.DGLGraph, in_feat: torch.Tensor) -> torch.Tensor:
        h = self.conv1(g, in_feat)
        h = F.softmax(h)
        h = self.conv2(g, h)
        h = F.relu(h)
        h = self.conv3(g, h)
        return h
