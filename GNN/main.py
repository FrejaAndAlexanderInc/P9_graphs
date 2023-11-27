import os
from GNN.gnn_model import HSAGE, NodeClassifier
from graph_builder.graph_builder import GraphBuilder
from graph_builder.model_constructor import ModelConstructor
import GNN.model_runner as runner
import torch as th

os.environ["DGLBACKEND"] = "pytorch"
import dgl
import numpy as np
import torch

# 'cpu' for cpu
# 'cuda' for gpu
device = 'cuda'  

def main():
    mc = ModelConstructor()
    # entities, relations, features = mc.build()
    g_builder = GraphBuilder(*mc.build())
    graph, node_labels = g_builder.create_graph()

    # Add reverse edges since ogbn-arxiv is unidirectional.
    # graph = dgl.add_reverse_edges(graph)


    node_labels = node_labels.float()
    graph.nodes['P'].data["label"] = node_labels
    # print(graph)
    # print(node_labels)

    # num_classes = (node_labels.max() + 1).item()
    # print("Number of classes:", num_classes)

    print(graph)
    # breakpoint()

    input_feature_size = 64  
    hidden_layer_size = 128
    num_classes = 2
    # features = runner.dummy_init_node_features(graph, 5)
    features = g_builder.get_features()

    # Create the GNN model
    # model = GNN(in_feats=input_feature_size, hidden_feats=hidden_layer_size, num_classes=num_classes)
    model = HSAGE(
        graph=graph,
        feats={},
        h_dim=5,
        out_dim=1,
        n_layers=3,
        dropout=0.001,
        device='cuda',
    )
    # model = NodeClassifier(in_feats=5, hidden_feats=64, out_feats=2, etypes=graph.etypes, dropout=0.001)

    # Train the GNN
    runner.train_gnn(model, graph, node_labels, features, epochs=1000)


if __name__ == '__main__':
    main()