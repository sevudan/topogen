#!/usr/sbin/python3.5


import networkx as nx
import matplotlib.pyplot as plt


def topology():
    """
    Function used for create new Graph.
    """ 
    total_nodes = 5
    number_of_rr = 1   
    logical_system = True
    if number_of_rr > 0:
        G = nx.DiGraph(name='Network topology - Star')
        starTopology(G,total_nodes, number_of_rr, logical_system)
    else: 
        G = nx.complete_graph(total_nodes)
        fullMeshTopology(G)
    nx.draw(G)
    return G, plt.show()

def genEdge(G, number_of_rr, logical_system, nodes):
    """
    Create edges attributes for Graph.
    """    
    if logical_system is True:
        ifd = 'lt'
    else:
        ifd = 'ge'
    if number_of_rr != 0:
        [*map(lambda node: nx.set_node_attributes(G, {node:{'role':'Router'}}), nodes[1:])]
        edges = tuple(zip(nodes[1:], map(lambda x: 0*x,nodes[1:])))
        G.add_edges_from(edges, ifd = '{}-0/0/1'.format(ifd))
        [*map(lambda edges,node: nx.set_edge_attributes(G, {edges: {'ifd':'{}-0/0/{}'.format(ifd,node)}}), G.edges(), nodes[1:])]        
    else:
        [*map(lambda edges, node: nx.set_edge_attributes(G, {edges: {'ifd':'{}-0/0/{}'.format(ifd, node)}}), G.edges(), nodes)]
    return G

def starTopology(G, total_nodes, number_of_rr, logical_system):
    """
    Function used for create Graph of type a star.
    
    """
    nodes = list(range(0,total_nodes + 1))
    nx.add_star(G, nodes)
    nx.set_node_attributes(G, {0: {'type':'Route-Reflector'}})
    genEdge(G, number_of_rr, logical_system, nodes)
    return G

def fullMeshTopology(G,number_of_rr,logical_system):
    """
    Generate new topology type of Full Mesh.
    """
    i = 0
    genEdge(G, number_of_rr,logical_system)
    return G


nx.draw(G, with_labels=True)
plt.show()


