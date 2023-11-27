import dgl
import torch
import torch.nn as nn
from GNN.gnn_model import HSAGE

def test_gnn(model: HSAGE, graph: dgl.DGLGraph, test_data: tuple[torch.Tensor, torch.Tensor]) -> None:
    features, labels = test_data
    logits = model(graph, features)

    # Assuming binary classification, calculate accuracy
    predictions = torch.argmax(logits, dim=1)
    accuracy = (predictions == labels).float().mean().item()

    print(f'Test Accuracy: {accuracy * 100:.2f}%')

def dummy_init_node_features(graph: dgl.DGLGraph, input_feature_size: int):
    # Initialize node features (replace with your actual initialization)
    # convention to use 'h' for 
    for node_type in graph.ntypes:
        graph.nodes[node_type].data['features'] = torch.zeros(graph.number_of_nodes(node_type), input_feature_size)

    return {node_type: torch.zeros(graph.number_of_nodes(node_type), input_feature_size) for node_type in graph.ntypes}

def train_gnn(model, graph: dgl.DGLGraph, labels: torch.Tensor, features, epochs: int) -> None:
    # Define loss function and optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(epochs):
        # Forward pass
        output_dict = model(graph, features)
        logits = output_dict['P']

        # Compute loss
        # Assuming labels are in the range [0, 1]
        loss = criterion(logits, labels.unsqueeze(1))  # Add unsqueeze to match the shape of logits

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}')