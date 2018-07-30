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
    logical_system = True
    if number_of_rr > 0:
        G = nx.Graph(name='Network topology - Star')
        starTopology(G,total_nodes, number_of_rr, logical_system)
    else: 
        G = nx.complete_graph(total_nodes)
        fullMeshTopology(G, number_of_rr,logical_system)
    return G.nodes(), logical_system

def genEdge(G, number_of_rr, logical_system):
    """
    Create edges attributes for Graph.
    """    
    if logical_system is True:
        ifd = 'lt'
    else:
        ifd = 'ge'
    num_router = 1
    if number_of_rr != 0:
        map(lambda num_router: nx.set_edge_attributes(G, {num_router:{'role':'Router'}}), G.edges())
        map(lambda x: nx.set_edge_attributes(G, {x: {'ifd':'{}-0/0/1'.format(ifd)}}), G.edges())
        map(lambda x,num_router: nx.set_edge_attributes(G, {x: {'ifd':'{}-0/0/{}'.format(ifd,num_router)}}), G.edges())        
    else:
        num_router = 0
        map(lambda num_router: nx.set_edge_attributes(G, {num_router: {'ifd':'{}-0/0/{}'.format(ifd, num_router)}}), G.edges())
    return G

def starTopology(G,total_nodes, number_of_rr, logical_system):
    """
    Function used for create Graph of type a star.
    """
    nodes = list(range(0,total_nodes + 1))
    nx.add_star(G, nodes)
    nx.set_node_attributes(G, {0: {'type':'Route-Reflector'}})
    genEdge(G, number_of_rr, logical_system)
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


