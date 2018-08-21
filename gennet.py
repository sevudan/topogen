import ipaddress as ip

def gen_loopback(lopool):
    """
    Generate Loopback address for nodes.
    """
    loopbacks = [str(x) for x in (ip.IPv4Network(lopool).hosts())]
    return loopbacks

def gen_ifaddress(ifpool):
    """
    Generate ipv4 address for eges.
    """
    arr = []
    for addr in ip.ip_network(ifpool).subnets(new_prefix=31):
        ipaddr = list(ip.IPv4Network(addr).hosts())
        arr.append(ipaddr)
    return arr
    