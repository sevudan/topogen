import gennet as net
import networkx as nx
import matplotlib.pyplot as plt
from ipaddress import *

"""
 ifd     Refers to a physical device
 ifl     Refers to a logical device
 iff     Refers to an address family
 ifa     Refers to an address entry
 iif     Refers to an incoming interface, either an ifd or an ifl 
         (uses a kernel interface index, not an SNMP index)
"""

lopool = '192.168.10.0/24'
ifpool = '10.250.0.0/23'

def topology(total_nodes = 5, number_of_rr = 1):
    """
    Function used for create new Graph.
    Execute this func first.
    """ 
    
    number = list(range(0,total_nodes + 1))
    nodes = sorted(list(map(lambda x: 'R{}'.format(x),number)))
    if number_of_rr > 0:
        G = nx.DiGraph(name='Network topology - Star')
        starTopology(G, nodes, number_of_rr, logical_system)
    else: 
        G = nx.complete_graph(total_nodes)
        fullMeshTopology(G)
    return G

def starTopology(G, nodes, number_of_rr, logical_system):
    """
    Function used for create Graph of type a star.
    """
    nx.add_star(G, nodes)
    loopbacks = net.genNet()
    #get loopback address for nodes
    loaddress = loopbacks.pop(0)    
    # set loopback addres for RR
    nx.set_node_attributes(G, {'R0': {'type':'Route-Reflector', 'loopback': loaddress}}) 
    # set loopback addres for other nodes
    [*map(lambda node: nx.set_node_attributes(G, {node: {'loopback':loaddress}}),nodes[1:])] 
    genEdge(G, nodes, logical_system)
    return G


def genEdge(G, nodes, loopbacks, logical_system=True):
    """
    Create edges attributes for Graph.
    """    
    if logical_system is True: ifd = 'lt'
    else: ifd = 'ge'
    edges_to_rr = zip(nodes[1:], map(lambda x: 'R{}'.format(0),nodes[1:]))
    ifl_num = range(0,len(edges_to_rr) + 1)
    [*map(lambda edges,ifl_num:
            nx.set_edge_attributes(
                G, {edges: {'ifd':'{}-0/0/{}'.format(ifd,ifl_num)}},
                sorted(G.edges()), ifl_num[1:]))
    ]
    G.add_edges_from(edges_to_rr, ifd = '{}-0/0/1'.format(ifd))
    return G

def genEdgeAddr():
    pool = net.genIFaddress(ifpool)
    ifa = {'local':pool[0],'nei':pool[1]}
    [*map(lambda edges,ifa:
            nx.set_edge_attributes(
                G, {edges: {'ip_address':'{}/31'.format(ifa)}},
                sorted(G.edges()), ifa[0]))
    ]


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


