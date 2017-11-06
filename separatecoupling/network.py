import networkx as nx
import matplotlib.pyplot as plt
import warnings

def construct():
    directed = input("Directed(d) or Undirected(u) graph? ")
    if directed == "d":
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edges = input("Enter edges in format:from_node to_node weight (Enter done to exist): ")
    while edges != "done":
        edge = edges.split()
        G.add_edge(edge[0],edge[1],weight=edge[2])
        edges = input("Enter edges in format:from_node to_node weight (Enter Done to exist): ")
    warnings.filterwarnings("ignore")
    #weights = nx.get_edge_attributes(G,'weight')
    if directed == "d":
        nx.draw_networkx(G, arrows=True)
    else:
        nx.draw(G)
    plt.show(block=False)
    return G

#construct()

