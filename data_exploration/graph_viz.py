import networkx as nx
import matplotlib.pyplot as plt
import dgl


def example_networkx_graph() -> nx.Graph:
    # Create a NetworkX graph (example)
    g = nx.Graph()
    g.add_nodes_from([1, 2, 3])
    g.add_edges_from([(1, 2), (2, 3), (1, 3)])
    return g


def visualize_dlg_graph(graph) -> None:
    nxg = graph.to_networkx()
    nx.draw(nxg, with_labels=True)
    plt.show()
