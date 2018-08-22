import gennet as net
import networkx as nx
import matplotlib.pyplot as plt
from ipaddress import *

"""
 Variable acronims:

 ifd     Refers to a physical device
 ifl     Refers to a logical device
 ifa     Refers to an address entry
 ce      customer edge (client)
"""

lopool = '192.168.10.0/24'
ifpool = '10.250.0.0/23'

def param():
    try:
        lopool = '192.168.10.0/24'
        ifpool = '10.250.0.0/23'
        total_nodes = 5 
        totalRR = 0
        total_ce = 2
        ls = True
        nodes = sum([total_nodes,total_ce])
        if nodes > 16:
            nodes/0 
        else:
            attr = {'lopool':lopool, 'ifpool':ifpool,
                    'total_nodes':total_nodes, 'totalRR':totalRR,
                    'total_ce':total_ce, 'ls':ls}
        return attr
    except ZeroDivisionError as error:
        return error

def topology():

    """
    Function used for create new Graph.
    Execute this func first.
    """

    try:
        param()
        if total_ce > 0:
            nodes_ce = sorted(map(
                                lambda x: 
                                    'CE{}'.format(x),range(0,total_ce)
                            ))
        #Generate nodes with name 'RX', where X is serial number 
        nodes = sorted(map(
                        lambda x:
                            'R{}'.format(x),range(0,total_nodes)
                        ))
        if totalRR > 0:
            G = nx.DiGraph(name='Network topology - Star')
            nx.add_star(G, nodes)
            gen_nodes(G, nodes, total_nodes, nodes_ce, ls)
            gen_edge(G, nodes, total_nodes, nodes_ce, ls)
        else: 
            G = nx.complete_graph(total_nodes)
            fullMeshTopology(G)
            gen_nodes(G, nodes, total_nodes, nodes_ce, ls)
            gen_edge(G, nodes, total_nodes, nodes_ce, ls)
        return G
    except ZeroDivisionError:
        print('Not valid total_nodes. Allowed  maximum 16 nodes!')

def gen_nodes(G, nodes, total_nodes, nodes_ce, ls):

    """
    Function for creating nodes and node attributes.
    """
    var = param()
    lopool = var[lopool]
    loopbacks = list(net.gen_loopback(lopool))[:total_nodes]
    # set loopback addres for RR
    nx.set_node_attributes(G, {'R0': {'type':'Route-Reflector', 'loopback':loopbacks.pop(0)}}) 
    # set loopback addres for other nodes
    [*map(
        lambda node, lo:
            nx.set_node_attributes(G, {node: {'loopback':lo}}), 
            nodes[1:], loopbacks
        )]            
    return G

def gen_edge(G, nodes, total_nodes, nodes_ce, ls):

    """
    Create edges attributes for nodes. Func create ip address and units
    for interface.
    """

    ifd = 'lt' if ls else 'ge'
    # To determine new edges for nodes between RR and R routers.
    edges_to_r = list(zip(map(lambda x: 'R0',nodes[1:]),
                        map(lambda x: '{}'.format(x),nodes[1:]))
                        )
    edges_to_rr = list(zip(nodes[1:], 
                        map(lambda x: 'R{}'.format(0),nodes[1:]))
                        )
    # Create new edges from R to RR.
    G.add_edges_from(edges_to_rr)
    # Get pool of ip address for edges.
    pool = gen_edge_addr(total_nodes)
    # Get list of units (ifl)
    total_edges = nx.number_of_edges(G)
    units = gen_edge_unit(total_edges)
    # Set interface and ip address for interface between RR and other routers.    
    ifl_num = range(1, len(edges_to_r)+1)
    [*map(
        lambda edges,ifl_num, ifa, unit, r_unit:
            nx.set_edge_attributes(G, 
                {edges: {'ifd':'{}-0/0/{}'.format(ifd,ifl_num),
                        'ip_address': '{}/31'.format(ifa),
                        'local_ifl':'{}'.format(unit),
                        'peer_ifl':'{}'.format(r_unit)}}
            ),
            edges_to_r, ifl_num, pool['local'], units['l_unit'], units['r_unit']
        )]
    # Set interface and ip address for interface between other routers and RR.
    G.add_edges_from(edges_to_rr, ifd = '{}-0/0/1'.format(ifd))
    [*map(
        lambda edges, ifa, unit, r_unit:
            nx.set_edge_attributes(G, 
                {edges: {'ip_address': '{}/31'.format(ifa),
                        'local_ifl': '{}'.format(unit),
                        'peer_ifl':'{}'.format(r_unit)}}
            ),
            edges_to_rr, pool['neighbor'], units['r_unit'], units['l_unit']
        )]
    return G

def gen_edge_addr(total_nodes):

    '''
    Function get ip address pool for interface.
    '''

    var = param()
    ifpool = var[ifpool]
    pool = list(net.gen_ifaddress(ifpool))[:total_nodes-1]
    local_ifa = [ str(x[0]) for x in pool ]
    neighbor_ifa = [ str(x[1]) for x in pool ]
    return {'local':local_ifa, 'neighbor':neighbor_ifa}

def gen_edge_unit(total_edges):

    '''
    Function get a logical number unit for interface.
    '''

    units = list(map(lambda var1,var2: [var1,var2] ,range(0,total_edges+1,2), range(1,total_edges+2,2)))
    local_ifl = [ x[0] for x in units ]
    neighbor_ifl = [ x[1] for x in units ]
    return {'l_unit':local_ifl, 'r_unit':neighbor_ifl}