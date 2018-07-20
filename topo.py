#!/usr/sbin/python3.5


import networkx as nx
import matplotlib.pyplot as plt

def __main__():
    pass


def createTopology():

    """
    Function used for create new Graph of type star or standart.
    """

    if number_of_rr > 0:
        G = nx.Graph(name='Network topology - Star')
        starTopology(G)
    else: 
        G = nx.Graph(name='Network topology - Basic')
        basicTopology(G)
    return G

def starTopology(G):
    """
    Function used for create Grapha of type a star.
    """

    total_nodes = 5
    number_of_rr = 1
    i = 0
    
    while i < total_nodes:
        nodes = list(range(i,total_nodes + 1))
        nx.add_star(G, nodes)
        attrs = 



while i < total_nodes:
    nodes = list(range(i,total_nodes + 1))
    if number_of_rr != 0:
        G.add_node(number_of_rr, role="Route-Reflector")
        for router in nodes:
            G.add_edge(number_of_rr,router,self_ifl="ge-0/0/{}".format(router))
        number_of_rr = 0
        i += 2
    else:
        G.add_nodes_from(nodes, role="Router")
        for router in nodes:
            G.add_edge(router,number_of_rr,self_ifl="ge-0/0/{}".format(number_of_rr)) 
        i = 5



nx.draw(G, with_labels=True)
plt.show()


