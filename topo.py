import random
import gennet as net
import networkx as nx
import matplotlib.pyplot as plt
from ipaddress import *

"""
    Variable acronims:
    ce      customer edge (client)
    pe      Provider edges node
    p       Core provider routers
    ce      customer edge
    ifd     Refers to a physical device
    ifl     Refers to a logical device
    ifa     Refers to an address entry
"""


def topology():

    """
    Function used for create new Graph.
    Execute this func first.
    """

    try:
        attr = param()
        core_nodes = attr['core_nodes']
        total_ce = attr['total_ce']
        ls = attr['ls']
        if total_ce > 0:
            nodes_ce = sorted(map(
                                lambda x: 
                                    'CE{}'.format(x),range(0,total_ce)
                            ))
        #Generate nodes with name 'RX', where X is serial number 
        nodes = sorted(map(
                        lambda x:
                            'R{}'.format(x),range(0,core_nodes)
                        ))
        if totalRR > 0:
            G = nx.DiGraph(name='Network topology - Star')
            nx.add_star(G, nodes)
            gen_core_nodes(G, nodes, core_nodes, nodes_ce, ls)
            gen_edge(G, nodes, core_nodes, nodes_ce, ls)
        else: 
            G = nx.complete_graph(core_nodes)
            gen_core_nodes(G, nodes, core_nodes, nodes_ce, ls)
            gen_edge(G, nodes, core_nodes, nodes_ce, ls)
        return G
    except AddressValueError as value_error:
        print('Error: {}'.format(value_error))
    except ZeroDivisionError:
        print('Not valid core_nodes. Allowed  maximum 16 nodes!')

def param():
    try:
        # chek ip_address
        lo_pool = str(IPv4Network('192.168.10.0/24'))
        ifpool = str(IPv4Network('10.250.0.0/23'))
        # set other params
        core_nodes = 5 
        totalRR = 1
        total_ce = 2
        ls = True
        nodes = sum([core_nodes,total_ce])
        if nodes > 16:
            nodes/0 
        else:
            attr = {'lo_pool':lo_pool, 'ifpool':ifpool, 'nodes':nodes,
                    'core_nodes':core_nodes, 'totalRR':totalRR,
                    'total_ce':total_ce, 'ls':ls}
        return attr
    except AddressValueError as value_error:
        return value_error
    except ZeroDivisionError as error:
        return error

def gen_core_nodes(G, nodes, core_nodes, ls):
    """
    Function for creating CORE nodes and attributes.
    """
    var = param()
    lo_pool = var['lo_pool']
    loopbacks = list(net.gen_loopback(lo_pool))[:core_nodes]
    # set loopback addres for RR
    nx.set_node_attributes(G, {'R0': {'type':'Route-Reflector', 'loopback':loopbacks.pop(0)}}) 
    # set loopback addres for other nodes
    [*map(
        lambda node, loopback:
            nx.set_node_attributes(G, {node: {'loopback':loopback}}), 
            nodes[1:], loopbacks
        )]            
    return G

def gen_edge_node(G, nodes, nodes_ce, ls):
    """
    Function for creating edges for nodes and attributes.
    """
    total_ce = len(nodes_ce)
    # choice CORE nodes for peers.
    pe_peers = random.sample(nodes, total_ce)
    edges_to_ce = list(zip(pe_peers, 
                        map(lambda x: 'CE{}'.format(x),range(total_ce)))
                        )
    G.add_edges_from(edges_to_ce)

def gen_edge(G, nodes, core_nodes, nodes_ce, ls):

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
    pool = gen_edge_addr(core_nodes)
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

def gen_edge_addr(core_nodes):

    '''
    Function get ip address pool for interface.
    '''

    var = param()
    ifpool = var[ifpool]
    pool = list(net.gen_ifaddress(ifpool))[:core_nodes-1]
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