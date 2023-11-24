import os
from GNN.gnn_model import HSAGE
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


    graph.nodes['P'].data["label"] = node_labels
    # print(graph)
    # print(node_labels)

    # num_classes = (node_labels.max() + 1).item()
    # print("Number of classes:", num_classes)

    

    input_feature_size = 64  

    # Create the GNN model
    # model = GNN(in_feats=input_feature_size, hidden_feats=hidden_layer_size, num_classes=num_classes)
    model = HSAGE(
        graph=graph,
        feats={},
        h_dim=128,
        out_dim=2,
        n_layers=3,
        dropout=0.001,
        device='cuda',
    )
    runner.dummy_init_node_features(graph, input_feature_size)

    # Train the GNN
    runner.train_gnn(model, graph, node_labels, epochs=100)




if __name__ == '__main__':
    main()