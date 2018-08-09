import gennet as net
import networkx as nx
import matplotlib.pyplot as plt
from ipaddress import *

"""
 Variable acronims:

 ifd     Refers to a physical device
 ifl     Refers to a logical device
 iff     Refers to an address family
 ifa     Refers to an address entry
 iif     Refers to an incoming interface, either an ifd or an ifl 
         (uses a kernel interface index, not an SNMP index)
"""

lopool = '192.168.10.0/24'
ifpool = '10.250.0.0/23'

def topology(total_nodes = 5, totalRR = 1, ls=True):
    """
    Function used for create new Graph.
    Execute this func first.
    """ 
    #Generate serial number for nodes
    number = list(range(0,total_nodes))
    #Generate nodes with name 'RX', where X is serial number 
    nodes = sorted(list(map(lambda x: 'R{}'.format(x),number)))
    if totalRR > 0:
        G = nx.DiGraph(name='Network topology - Star')
        nx.add_star(G, nodes)
        gen_nodes(G, nodes, total_nodes, totalRR, ls=True)
        gen_edge(G, nodes, total_nodes, ls=True)
    else: 
        G = nx.complete_graph(total_nodes)
        fullMeshTopology(G)
    return G

def gen_nodes(G, nodes, total_nodes, ls):
    """
    Function for creating nodes and node attributes.
    """
    loopbacks = list(net.gen_loopback(lopool))[:total_nodes]
    # set loopback addres for RR
    nx.set_node_attributes(G, {'R0': {'type':'Route-Reflector', 'loopback':loopbacks.pop(0)}}) 
    # set loopback addres for other nodes
    [*map(lambda node, lo: nx.set_node_attributes(G, {node: {'loopback':lo}}), nodes[1:], loopbacks)] 
    return G

def gen_edge(G, nodes, total_nodes, ls):
    """
    Create edges attributes for nodes. Func create ip address and units
    for interface.
    """
    ifd = 'lt' if ls else 'ge'
    # To determine new edges for nodes between RR and R routers.
    edges_to_r = list(zip(map(lambda x: 'R0',nodes[1:]),
                        map(lambda x: '{}'.format(x),nodes[1:]))
                    )
    edges_to_rr = list(zip(nodes[1:], map(lambda x: 'R{}'.format(0),nodes[1:])))
    # Get pool of ip address for edges.
    pool = gen_edge_addr(total_nodes)
    # Get list of units (ifl)
    total_edges = nx.number_of_edges(G)
    units = gen_edge_unit(total_edges)
    # Create new edges from R to RR.
    G.add_edges_from(edges_to_rr)
    # Set interface and ip address for interface between RR and other routers.    
    ifl_num = range(0, len(edges_to_r) + 1)
    [*map(lambda edges,ifl_num, ifa:
        nx.set_edge_attributes(G, 
            {edges:  {'ifd':'{}-0/0/{}'.format(ifd,ifl_num),
                      'ip_address': '{}/31'.format(ifa)}
            }),
            edges_to_r, ifl_num[1:], pool['local'])]
    # Set interface and ip address for interface between other routers and RR.
    G.add_edges_from(edges_to_rr, ifd = '{}-0/0/1'.format(ifd))
    [*map(lambda edges, ifa:
        nx.set_edge_attributes(G, {edges: {'ip_address': '{}/31'.format(ifa)}}),
        edges_to_rr, pool['neighbor'])]
    return G

def gen_edge_addr(total_nodes):
    pool = list(net.gen_ifaddress(ifpool))[0:total_nodes]
    local_ifa = [ str(x[0]) for x in pool ]
    neighbor_ifa = [ str(x[1]) for x in pool ]
    return {'local':local_ifa, 'neighbor':neighbor_ifa}

def gen_edge_unit(total_edges):
    units = list(map(lambda var1,var2: [var1,var2] ,range(0,total_edges+1,2), range(1,total_edges+2,2)))
    local_ifl = [ x[0] for x in units ]
    neighbor_ifl = [ x[1] for x in units ]
    return {'l_unit':local_ifl, 'r_unit':neighbor_ifl}