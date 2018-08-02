import topo
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
    template = Template(data)
    return(template)

def getParams():
    """
    Get parametrs from Graph.
    """
    num = nx.number_of_edges(G)
    ifl  = list(range(0,num+1,2))
    pifl = list(range(1,num+2,2))
    return(ifl, pifl)

def genConfig():
    """
    Write result into file $PATH/result.cfg
    """
    getTemplate()
    getParams()
    nodes = sorted(G.nodes())
    node = [*map(lambda hostname: template.render(node=hostname), nodes)]
    [*map(lambda unit: template.render(unit=ifl)), ifl]
    [*map(lambda runit: template.render(runit=pifl)), pifl]
    result = '\n'.join(node)
    with open('/home/sevudan/Scripts/projects/topogen/result.cfg','w') as cfg:
        cfg.write(result)
    cfg.close()