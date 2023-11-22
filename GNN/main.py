import os
from graph_builder.graph_builder import GraphBuilder
from graph_builder.model_constructor import ModelConstructor

os.environ["DGLBACKEND"] = "pytorch"
import dgl
import numpy as np
import torch

device = "gpu"  # change to 'cuda' for GPU

def main():
    mc = ModelConstructor()
    # entities, relations, features = mc.build()
    g_builder = GraphBuilder(*mc.build())
    node_labels = g_builder.get_labels()
    graph = g_builder.create_graph()

    # Add reverse edges since ogbn-arxiv is unidirectional.
    # graph = dgl.add_reverse_edges(graph)
    graph.ndata["label"] = node_labels#[:, 0]
    print(graph)
    print(node_labels)

    node_features = graph.ndata["feat"]
    num_features = node_features.shape[1]
    num_classes = (node_labels.max() + 1).item()
    print("Number of classes:", num_classes)

if __name__ == '__main__':
    main()