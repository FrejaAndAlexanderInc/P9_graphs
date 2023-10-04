import os

from gcn_3layer import GCN3L
os.environ["DGLBACKEND"] = "pytorch"

import dgl
import dgl.data
import torch
import torch.nn as nn
import torch.nn.functional as F
import networkx as nx
from dgl.nn import GraphConv
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score

CUDA = True

class GCN(nn.Module):
    """Example 2 layer GCN
    """

    def __init__(self, in_feats: int, h_feats: int, num_classes: int):
        """
        Args:
            in_feats (int): number of input features for each node 
            h_feats (int): number of hidden features or dimensions in the intermediate GCN layer
            num_classes (int): number of output classes or categories in the classification task
        """
        super(GCN, self).__init__()
        self.conv1 = GraphConv(in_feats, h_feats)
        self.conv2 = GraphConv(h_feats, num_classes)

    def forward(self, g: dgl.DGLGraph, in_feat: torch.Tensor) -> torch.Tensor:
        """defines the forward pass of the GCN model. 
        It specifies how the input data should be transformed as it passes through the layers.

        Args:
            g (dgl.DGLGraph): input graph 
            in_feat (torch.Tensor): node features as a Tensor 

        Returns:
            torch.Tensor: unnormalized scores for each class
        """
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = self.conv2(g, h)
        return h


# dataset 
dataset = dgl.data.CoraGraphDataset()
print(f"Number of categories: {dataset.num_classes}")

# A DGL Dataset object may contain one or multiple graphs. 
# The Cora dataset used only consists of one single graph.
graph = dataset[0]

print("Node features")
print(graph.ndata['train_mask'])
print("Edge features")
print(graph.edata.keys())
print(graph.ndata['feat'][0])

def train(g, model, epochs=100, learning_rate=0.01):
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    best_val_acc = 0
    best_test_acc = 0

    features = g.ndata["feat"]
    labels = g.ndata["label"]
    train_mask = g.ndata["train_mask"]
    val_mask = g.ndata["val_mask"]
    test_mask = g.ndata["test_mask"]

    for e in range(epochs):
        # Forward
        logits = model(g, features)

        # Compute prediction
        pred = logits.argmax(1)

        # Compute loss
        # Note that you should only compute the losses of the nodes in the training set.
        loss = F.cross_entropy(logits[train_mask], labels[train_mask])

        # Compute accuracy on training/validation/test

        # f1 for validation and test set is done each epoch
        train_f1 = f1_score(labels[train_mask].cpu().numpy(), pred[train_mask].cpu().numpy(), average='macro')
        val_f1 = f1_score(labels[val_mask].cpu().numpy(), pred[val_mask].cpu().numpy(), average='macro')
        test_f1 = f1_score(labels[test_mask].cpu().numpy(), pred[test_mask].cpu().numpy(), average='macro')

        # train_acc = (pred[train_mask] == labels[train_mask]).float().mean()
        # val_acc = (pred[val_mask] == labels[val_mask]).float().mean()
        # test_acc = (pred[test_mask] == labels[test_mask]).float().mean()

        # Save the best validation accuracy and the corresponding test accuracy.
        if best_val_acc < val_f1:
            best_val_acc = val_f1
            best_test_acc = test_f1

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if e % 5 == 0:
            print(
                f"In epoch {e}, loss: {loss:.3f}, val f1: {val_f1:.3f} (best {best_val_acc:.3f}), test f1: {test_f1:.3f} (best {best_test_acc:.3f})"
            )


model = GCN(graph.ndata["feat"].shape[1], 32, dataset.num_classes)
model3l = GCN3L(graph.ndata["feat"].shape[1], 32, 16, dataset.num_classes)

if CUDA:
    graph = graph.to('cuda')
    model = model.to('cuda')
    model3l = model.to('cuda')

train(graph, model3l, 100, 0.01)