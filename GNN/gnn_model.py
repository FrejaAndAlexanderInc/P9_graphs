import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn.pytorch import GraphConv

class GNN(nn.Module):
    def __init__(self, in_feats, hidden_feats, num_classes):
        super(GNN, self).__init__()
        self.conv1 = GraphConv(in_feats, hidden_feats)
        self.conv2 = GraphConv(hidden_feats, hidden_feats)
        self.fc = nn.Linear(hidden_feats, num_classes)

    def forward(self, g: dgl.DGLGraph, features: torch.Tensor) -> torch.Tensor:
        # Apply graph convolutional layers
        x = F.relu(self.conv1(g, features))
        x = F.relu(self.conv2(g, x))

        # Global pooling (sum or mean) to obtain a graph-level representation
        x = dgl.mean_nodes(g, x)

        # Fully connected layer for classification
        x = self.fc(x)

        return x