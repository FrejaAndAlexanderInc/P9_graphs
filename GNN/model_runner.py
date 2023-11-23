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

def dummy_init_node_features(graph: dgl.DGLGraph, input_feature_size: int) -> None:
    # Initialize node features (replace with your actual initialization)
    for node_type in graph.ntypes:
        graph.nodes[node_type].data['features'] = torch.randn(graph.number_of_nodes(node_type), input_feature_size)

def train_gnn(model: HSAGE, graph: dgl.DGLGraph, labels: torch.Tensor, epochs: int) -> None:
    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(epochs):
        # Forward pass
        logits = model(graph, graph.nodes['P'].data['features'])

        # Compute loss
        loss = criterion(logits, labels)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Print the loss for monitoring
        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}')