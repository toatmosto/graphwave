import networkx as nx 
import matplotlib.pyplot as plt

def get_hop1_neighbors(node, graph, get_only_edges_to_node=False, plot=True, verbose=False):
    all_neighbors = set(graph[node])
    all_nodes = all_neighbors.copy()
    all_nodes.add(node)
    subgraph = graph.subgraph(all_nodes)
    all_edges = set(subgraph.edges)

    if get_only_edges_to_node:
        # assuming undirected edges
        edges_to_plot = set([(node, y) for y in all_neighbors])
    else:
        edges_to_plot = all_edges
    node_color = ['yellow'] * len(all_nodes)
    node_color[list(subgraph.nodes).index(node)] = 'red'
    if plot:
        nx.draw_networkx(subgraph,
                         node_color=node_color,
                         edgelist=edges_to_plot,
                         alpha=0.5)        
        plt.show()
    if verbose:
        print("For node {}:".format(node))
        print("{} hop1 neighbors: {}".format(len(all_neighbors), all_neighbors))
        print("{} hop1 edges to plot: {}".format(len(edges_to_plot), edges_to_plot))
        print("\n")
    return all_neighbors, edges_to_plot

def get_hop2_neighbors(node, graph, get_only_edges_to_node_hop1=False,
                       get_only_edges_to_node_hop2=False, plot=True, verbose=False):
    # get hop1 neighbors and edges
    hop1_neighbors, hop1_edges = get_hop1_neighbors(
        node, graph, get_only_edges_to_node_hop1, plot=False, verbose=verbose)
    hop2_neighbors = set()
    hop2_edges = set()
    
    # get hop 2 neighbors and edges
    for hop1_nb in hop1_neighbors:
        nbs, edges = get_hop1_neighbors(hop1_nb,
                                        graph,
                                        get_only_edges_to_node_hop2,
                                        plot=False,
                                        verbose=False)
        if verbose:
            print("For hop1 neighbor {}".format(hop1_nb))
            print("{} hop2 neighbors: {}".format(len(nbs), nbs))
            print("{} hop2 edges to plot: {}".format(len(edges), edges))
            print("\n")
        hop2_neighbors = hop2_neighbors.union(nbs)
        hop2_edges = hop2_edges.union(edges)

    # get all nodes and edges
    all_nodes = hop1_neighbors.union(hop2_neighbors)
    all_nodes.add(node)
    subgraph = graph.subgraph(all_nodes)
    edges_to_plot = hop1_edges.union(hop2_edges)

    # node color
    node_color = ['yellow'] * len(all_nodes)
    node_color[list(subgraph.nodes).index(node)] = 'red'
    for hop1_nb in hop1_neighbors:
        node_color[list(subgraph.nodes).index(hop1_nb)] = 'green'

    if plot:
        nx.draw_networkx(subgraph,
                         node_color=node_color,
                         edgelist=edges_to_plot,
                         alpha=0.5)

    return hop1_neighbors, hop2_neighbors, hop1_edges, hop2_edges