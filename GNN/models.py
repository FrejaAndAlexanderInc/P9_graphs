import dgl
import torch as th
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn.pytorch import SAGEConv, HeteroGraphConv, GraphConv

import torch.nn as nn
import torch.nn.functional as F

class GraphSAGE(nn.Module):
    def __init__(self, in_feats: int, hidden_feats: int, out_feats: int, etypes, dropout: float):
        super(GraphSAGE, self).__init__()
        # self.conv1 = SAGEConv(in_feats, hidden_feats, aggregator_type='mean')
        # self.conv2 = SAGEConv(hidden_feats, out_feats, aggregator_type='mean')
        self.input_layer = SAGEConvLayer(in_feats, hidden_feats, etypes, dropout)
        self.output_layer = SAGEConvLayer(hidden_feats, out_feats, etypes, dropout)

        # Convolutions
        self.layers = nn.ModuleList()
        self.layers.append(self.input_layer)
        for _ in range(1):
            self.layers.append(
                SAGEConvLayer(
                    hidden_feats,
                    hidden_feats,
                    etypes,
                    dropout
                )
            )
        self.layers.append(self.output_layer)

        self.activation = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, g: dgl.DGLGraph, features: dict[str, th.Tensor]) -> dict[str, th.Tensor]:
        h_dict = {}
        for edge_type, conv in self.input_layer.items():
            src, dst = g.all_edges(etype=edge_type)
            h = conv(g, features[edge_type], src, dst)
            h_dict[edge_type] = F.relu(h)

        for edge_type, conv in self.output_layer.items():
            src, dst = g.all_edges(etype=edge_type)
            h = conv(g, h_dict[edge_type], src, dst)
            h_dict[edge_type] = F.relu(h)

        # Perform mean pooling for each node type separately
        pooled_dict = {}
        for node_type in g.ntypes:
            # Get the nodes of the current type
            nodes = g.nodes(node_type)

            # Extract the corresponding hidden features
            hidden_feats = [h_dict[edge_type][nodes] for edge_type in g.etypes if edge_type[0] == node_type]

            # Perform mean pooling
            pooled_feats = th.mean(th.stack(hidden_feats), dim=0)
            pooled_dict[node_type] = pooled_feats

        return pooled_dict

    # def forward(self, g: dgl.DGLGraph, features) -> dict[str, th.Tensor]:
    #     # Use the same GraphSAGE-like model for each edge type
    #     h_dict = self.conv1(g, features)
    #     h_dict = {k: F.relu(h) for k, h in h_dict.items()}
    #     h_dict = self.conv2(g, h_dict)
    #     h_dict = {k: F.relu(h) for k, h in h_dict.items()}
        
    #     # Global pooling (sum or mean) to obtain a graph-level representation
    #     h = dgl.mean_nodes(g, 'features', h_dict, ntype=g.ntypes)
    #     return h

class NodeClassifier(nn.Module):
    def __init__(self, in_feats: int, hidden_feats: int, out_feats: int, etypes, dropout: float):
        super(NodeClassifier, self).__init__()
        self.gnn = GraphSAGE(in_feats, hidden_feats, out_feats, etypes, dropout)
        self.fc = nn.Linear(out_feats, 1)  # Binary classification
    
    def forward(self, g: dgl.DGLGraph, features: dict[str, th.Tensor]) -> th.Tensor:
        h = self.gnn(g, features)
        logits = self.fc(h)
        return logits.squeeze(1)

class HSAGE(nn.Module):
    def __init__(
            self,
            graph: dgl.DGLGraph,
            feats,
            h_dim: int,
            out_dim: int,
            n_layers: int,
            dropout: float,
            device: str,
            loss_func=None,
            extras=None):
        super().__init__()
        self.h_dim = h_dim
        self.out_dim = out_dim
        self.n_layers = n_layers
        self.dropout = dropout
        self.etypes = graph.etypes
        self.ntypes = graph.ntypes
        self.extras = extras
        self.loss_func = loss_func
        self.device = device
        self.feats = nn.ParameterDict()
        self.input = nn.ModuleDict({})
        self.out_layer = None

        self.preprocess(graph, feats)

        # Convolutions
        self.layers = nn.ModuleList()
        for _ in range(self.n_layers):
            self.layers.append(SAGEConvLayer(
                self.h_dim,
                self.h_dim,
                self.etypes,
                self.dropout))

        self.activation = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

        # linear output layer for base predictions
        self.set_output_layer(self.out_dim)

        # Here we modify the model if something special is required
        if self.loss_func == 'hmcn_out':
            # Here we create a layer to transform the final output
            # into hierarchical classifications (one for each hierarchy)
            self.flat_hml = nn.ModuleDict({
                name: nn.Linear(self.h_dim, len(dim)) for name, dim in self.extras['rollup_maps'].items()
            })

    def freeze_gcn_layer(self, layer):
        for param in self.layers[layer].parameters():
            param.requires_grad = False

    def set_output_layer(self, out_dim):
        self.out_layer = nn.Linear(self.h_dim, out_dim)

    def add_gcn_layer(self):
        self.layers.append(SAGEConvLayer(
            self.h_dim,
            self.h_dim,
            self.etypes,
            self.dropout))

    def preprocess(self, graph, feats):
        # Keep track of dims for subsequent linear transformations
        linear_dict = {}

        # Assign trainable embeddings
        if feats == {}:
            print("Assigning trainable embeddings to nodes")
            for ntype in graph.ntypes:
                self.feats[ntype] = self.create_type_emb(graph.number_of_nodes(ntype), self.h_dim)
                linear_dict[ntype] = [self.h_dim, self.h_dim]

        # Extract existing embeddings
        else:
            print('Embeddings already preinitialized')
            for ntype in graph.ntypes:
                if feats.get(ntype) is None:
                    self.feats[ntype] = self.create_type_emb(graph.number_of_nodes(ntype), self.h_dim)
                    linear_dict[ntype] = [self.h_dim, self.h_dim]
                else:
                    self.feats[ntype] = nn.Parameter(feats.get(ntype), requires_grad=False)
                    linear_dict[ntype] = [self.feats[ntype].shape[1], self.h_dim]

        # Type-specific linear transformations for semantic integration
        self.add_linear_trans(linear_dict)

    def add_linear_trans(self, linear_dict):
        for ntype, (in_dim, out_dim) in linear_dict.items():
            self.input[ntype] = nn.Linear(in_dim, out_dim)

    def create_type_emb(self, num_nodes, emb_dim):
        emb = nn.Parameter(th.Tensor(num_nodes, emb_dim))
        nn.init.xavier_uniform_(emb, gain=nn.init.calculate_gain('relu'))
        return emb

    def forward(self, graph: dgl.DGLGraph, feats: dict[str, th.Tensor]):

        if type(graph) != list:
            # full graph training,
            for layer_id, layer in enumerate(self.layers):
                # Do convolution
                feats = layer(graph, feats)

                # Apply activation function
                feats = {k: self.activation(v) for k, v in feats.items()}

        else:
            # minibatch training, block
            for layer, block in zip(self.layers, graph):

                # Apply convolution
                feats = layer(block, feats)

                # Apply activation function
                feats = {k: self.activation(v) for k, v in feats.items()}

        # If we need to do something special, we do it here
        if self.loss_func == 'hmcn_out':
            # Perform multiple output calculations,
            # One for each hierarchical level
            for name, layer in self.flat_hml.items():
                feats[name] = self.sigmoid(layer(feats['P']))

        # linear output layer
        feats['P'] = self.sigmoid(self.out_layer(feats['P']))
        # return self.sigmoid(self.out_layer(feats['P']))

        return feats

    def freeze_parameters(self):
        for type in self.ntypes:
            self.input_feature.embed_dict[type].requires_grad = False


class SAGEConvLayer(nn.Module):
    def __init__(
            self,
            in_dim,
            out_dim,
            etypes,
            dropout):
        super(SAGEConvLayer, self).__init__()

        # Definition of HeteroGraphConv SAGE Layer
        self.layer = HeteroGraphConv(
                {rel: SAGEConv(
                    in_feats=in_dim,
                    out_feats=out_dim,
                    feat_drop=dropout,
                    aggregator_type='mean'
                ) for rel in etypes}
            )

    def forward(self, mfg, h):
        return self.layer(mfg, h)

class GNN2layer(nn.Module):
    def __init__(self, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

