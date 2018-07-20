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
    if number_of_rr > 0:
        G = nx.Graph(name='Network topology - Star')
        starTopology(G,number_of_rr)
    else: 
        G = nx.Graph(name='Network topology - Full fullMeshTopology')
        fullMeshTopology(G)
    return G.edges()

def starTopology(G, number_of_rr,total_nodes):
    """
    Function used for create a Graph of type a star.
    """
    i = 1
    nodes = list(range(0,total_nodes + 1))
    nx.add_star(G, nodes)
    nx.set_node_attributes(G, {0: {'type':'Route-Reflector'}})
    while i < total_nodes:
        nx.set_node_attributes(G, {i:{'role':'Router'}})
        nx.set_edge_attributes(G, {(i,0): {'ifd':'ge-0/0/1'}})
        nx.set_edge_attributes(G, {(0,i): {'ifd':'ge-0/0/{}'.format(i)}})
        i += 1
    return G

def fullMeshTopology(G):
    pass


"""
while i < total_nodes:
    nodes = list(range(i,total_nodes + 1))
    if number_of_rr != 0:
        G.add_node(number_of_rr, role="Route-Reflector")
        for router in nodes:
            G.add_edge(number_of_rr,router,self_ifd="ge-0/0/{}".format(router))
        number_of_rr = 0
        i += 2
    else:
        G.add_nodes_from(nodes, role="Router")
        for router in nodes:
            G.add_edge(router,number_of_rr,self_ifd="ge-0/0/{}".format(number_of_rr)) 
        i = 5
"""


nx.draw(G, with_labels=True)
plt.show()


