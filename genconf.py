import itertools
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
    with open('/home/sevudan/Scripts/projects/topogen/template.cfg') as file:
        data = file.read()
    return Template(data)
    

def getParams(*arg):
    """
    Get parametrs from Graph.
    """
    # Get total number of edges
    num = nx.number_of_edges(G)
    # Get list the edges 
    edges = [ list(x) for x in G.edges() ]
    
    '''revers = (map(lambda var1,var2: [var1,var2][::-1] ,range(0,num+1,2), range(1,num+2,2)))
    pifl = list(itertools.chain.from_iterable(revers))
    ifl = list(range(0,num+1))'''
    return {'unit':ifl, 'punit':pifl}

def genConfig():
    """
    Write result into file $PATH/result.cfg.
    Execute this func first.
    """
    template = getTemplate()
    for x in G.nodes:
        d = dict(G[x])
        hostname = x
        peer = d.keys()
        for x in peer:
            params = d.get(x)
            conf = template.render(node=hostname,pu=punit, 
                                    ifd = params.get('ifd'),
                                    ip_address = params.get('ip_address'),
                                    ifl = params.get('unit'))
            result = '\n'.join(conf)
    with open('/home/sevudan/Scripts/projects/topogen/result.cfg','w') as cfg:
        cfg.write(result)
    cfg.close()