#!/usr/sbin/python3.5


import networkx as nx
import matplotlib.pyplot as plt

def __main__():
    pass


def topology():
    """
    Function used for create new Graph.
    """
    total_nodes = 5
    number_of_rr = 1
    onerouter = True
    if number_of_rr > 0:
        G = nx.Graph(name='Network topology - Star')
        starTopology(G,number_of_rr)
    else: 
        G = nx.complete_graph(total_nodes)
        fullMeshTopology(G)
    return G.edges(), onerouter

def genEdge(i, number_of_rr, total_nodes, onerouter):
    """
    Create edges for Graph.
    """
    if onerouter is True:    
        i = 0
        while i < total_nodes:
            if number_of_rr == 0:
                nx.set_node_attributes(G, {i:{'role':'Router'}})
                nx.set_edge_attributes(G, {(i,0): {'ifd':'ge-0/0/1'}})
                nx.set_edge_attributes(G, {(0,i): {'ifd':'ge-0/0/{}'.format(i)}})
                i += 1
            else:
                nx.set_edge_attributes(G, {(0,i): {'ifd':'ge-0/0/{}'.format(i)}})
                i += 1
    else:
        pass

def starTopology(G, number_of_rr, total_nodes, onerouter):
    """
    Function used for create Graph of type a star.
    """
    nodes = list(range(0,total_nodes + 1))
    nx.add_star(G, nodes)
    nx.set_node_attributes(G, {0: {'type':'Route-Reflector'}})
    i = 1
    genEdge(i, number_of_rr, total_nodes)

def fullMeshTopology(G, total_nodes):
    """
    Generate new topology type of Full Mesh.
    """
    i = 0
    genEdge(i, number_of_rr, total_nodes)


nx.draw(G, with_labels=True)
plt.show()


