import topo
import networkx as nx
import matplotlib.pyplot as plt
from jinja2 import Template    
"""
 Variable acronims:

 ifd     Refers to a physical device
 ifl     Refers to a logical device
 iff     Refers to an address family
 ifa     Refers to an address entry
 iif     Refers to an incoming interface, either an ifd or an ifl 
         (uses a kernel interface index, not an SNMP index)
"""    

def getTemplate():

    """ 
    Get template from from file $PATH/template.cfg
    """

    with open('/home/sevudan/Scripts/projects/topogen/template.cfg', 'r') as file:
        data = file.read()
        file.close()
    return Template(data)

def draw_topology(G):

    """
    Draw topology.
    """
    
    pos = nx.spring_layout(G)
    for p in pos:  # raise text positions
        pos[p][1] += 0.07
    nx.draw_networkx_labels(G, pos)
    edge_labels = nx.get_edge_attributes(G,'ifd')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, pos, font_size=16, with_labels=False)
    return(plt.show())

def gen_config_lo(G, cfg):

    """
    Generate loopback interfaces with loopback and units for nodes.
    """

    lo_ifl = 0
    for node in sorted(G.nodes):
        d = dict(G[node])
        hostname = node
        loopback = G.node[node].get('loopback')
        set_loopback = Template('set logical-systems {{ node }} interfaces lo0.{{ loopback_ifl }} family inet address {{ loopback_ifa }}')
        result = set_loopback.render(
                                    node = hostname, 
                                    loopback_ifl = lo_ifl, 
                                    loopback_ifa = loopback
                                    )
        result = '{}{}'.format(result,'\n')
        cfg.write(result) 
        lo_ifl += 1

def genConfig():

    """
    Generate config for all nodes from template.
    Write result into file $PATH/result.cfg.
    """

    cfg = open('/home/sevudan/Scripts/projects/topogen/result.cfg','w')
    template = getTemplate()
    G = topo.topology()
    gen_config_lo(G, cfg)
    # Get node from list nodes.
    for node in sorted(G.nodes):
        d = dict(G[node])
        hostname = node
        # Get attributes for node.
        peer = d.keys()
        for peer_node in peer:
            params = d.get(peer_node)
            conf = template.render(
                                    node=hostname,
                                    description = peer_node,
                                    ifd = params.get('ifd'),
                                    local_ifl = params.get('local_ifl'),
                                    peer_ifl = params.get('peer_ifl'),
                                    ifa = params.get('ip_address')
                                    )
            result = '{}{}'.format(conf,'\n')
            cfg.write(result)
    cfg.close()

genConfig()