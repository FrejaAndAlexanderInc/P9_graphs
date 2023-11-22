import os
from GNN.gnn_model import GNN
from graph_builder.graph_builder import GraphBuilder
from graph_builder.model_constructor import ModelConstructor
import GNN.model_runner as runner

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

    # should be tuned 
    input_feature_size = 64  
    hidden_layer_size = 128
    num_classes = 2 

    # Create the GNN model
    model = GNN(in_feats=input_feature_size, hidden_feats=hidden_layer_size, num_classes=num_classes)
    runner.dummy_init_node_features(graph, input_feature_size)

    # Create labels (0 or 1) for binary classification
    labels = torch.randint(0, 2, (graph.number_of_nodes('P'),))

    # Train the GNN
    runner.train_gnn(model, graph, labels, epochs=10)


if __name__ == '__main__':
    main()