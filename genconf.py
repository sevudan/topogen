import topo
import networkx as nx
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
def genConfig():
    """
    Write result into file $PATH/result.cfg.
    Execute this func first.
    """
    cfg = open('/home/sevudan/Scripts/projects/topogen/result.cfg','w')
    template = getTemplate()
    G = topo.topology()
    for node in G.nodes:
        d = dict(G[node])
        hostname = node
        peer = d.keys()
        for peer_node in peer:
            params = d.get(peer_node)
            conf = template.render(node=hostname,
                                    description = peer_node,
                                    ifd = params.get('ifd'),
                                    local_ifl = params.get('local_ifl'),
                                    peer_ifl = params.get('peer_ifl'),
                                    ip_address = params.get('ip_address'))
            result = '{}{}'.format(conf,'\n')
            cfg.write(result)
    cfg.close()
    print('Done')
genConfig()