import topo
import itertools
import networkx as nx
import ipaddress as ip
from jinja2 import Template


pool = '192.168.10.0/24'
ifl = '0'  #unit number
iface_addr = ''  #interface ip pool
pu = '' #pear unit for interfaces

loopbacks = [str(x) for x in (ip.IPv4Network(pool).hosts())]


def getTemplate():
    """ 
    Get template from from file $PATH/template.cfg
    """
    with open('/home/sevudan/Scripts/projects/topogen/template.cfg') as file:
        data = file.read()
    return Template(data)
    

def getParams():
    """
    Get parametrs from Graph.
    """
    num = nx.number_of_edges(G)
    revers = (map(lambda var1,var2: [var1,var2][::-1] ,range(0,num+1,2), range(1,num+2,2)))
    pifl = list(itertools.chain.from_iterable(revers))
    ifl = list(range(0,num+1))
    return {'unit':ifl, 'punit':pifl}

def genConfig():
    """
    Write result into file $PATH/result.cfg.
    Execute this func first.
    """
    template = getTemplate()
    units = getParams()
    nodes = sorted(G.nodes())
    lunit = [*map(lambda hostname,unit,punit: template.render(node=hostname,ifl=unit,pu=punit), nodes, units['unit'], units['punit'])]
    result = '\n'.join(lunit)
    with open('/home/sevudan/Scripts/projects/topogen/result.cfg','w') as cfg:
        cfg.write(result)
    cfg.close()