#!/usr/sbin/python3.5

import gennet as net
import networkx as nx
import matplotlib.pyplot as plt


def topology():
    """
    Function used for create new Graph.
    Execute this func first.
    """ 
    total_nodes = 5
    number_of_rr = 1   
    logical_system = True
    number = list(range(0,total_nodes + 1))
    nodes = sorted(list(map(lambda x: 'R{}'.format(x),number)))
    if number_of_rr > 0:
        G = nx.DiGraph(name='Network topology - Star')
        starTopology(G, nodes, number_of_rr, logical_system)
    else: 
        G = nx.complete_graph(total_nodes)
        fullMeshTopology(G)
    return G

def genStarEdge(G, nodes, loopbacks, logical_system):
    """
    Create edges attributes for Graph.
    """    
    if logical_system is True: 
        ifd = 'lt'
    else: 
        ifd = 'ge'
    edges_to_rr = zip(nodes[1:], map(lambda x: 'R{}'.format(0),nodes[1:]))
    ifl_num = range(0,len(edges_to_rr) + 1)
    [*map(lambda edges,ifl_num: 
            nx.set_edge_attributes(
                G, {edges: {'ifd':'{}-0/0/{}'.format(ifd,ifl_num)}}
                ),
                sorted(G.edges()), ifl_num[1:]
                )]
    G.add_edges_from(edges_to_rr, ifd = '{}-0/0/1'.format(ifd))
    return G
    """
    else:
        [*map(lambda edges, node: nx.set_edge_attributes(G, {edges: {'ifd':'{}-0/0/{}'.format(ifd, node)}}), G.edges(), nodes)]
    
    return G
    """
def starTopology(G, nodes, number_of_rr, logical_system):
    """
    Function used for create Graph of type a star.
    """
    nx.add_star(G, nodes)
    loopbacks = net.genNet()
    rrlo = ipaddr.pop(0)
    nx.set_node_attributes(G, {'R0': {'type':'Route-Reflector', 'loopback': rrlo}})
    [*map(lambda node: 
            nx.set_node_attributes(
                G, {node: {'loopback':loopbacks}}
                ),
                nodes[1:]
                )]
    genStarEdge(G, nodes, logical_system)
    return G

"""
def fullMeshTopology(G,number_of_rr,logical_system):
    
    Generate new topology type of Full Mesh.
    
    i = 0
    genEdge(G, number_of_rr,logical_system)
    return G

node_labels = nx.get_edge_attributes(G, 'ifd')
nx.draw_networkx_labels(G, pos, node_labels)
nx.draw(G, with_labels=True)
plt.show()
"""


