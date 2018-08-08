import ipaddress as ip

def genLoopback(lopool):
	loopbacks = [str(x) for x in (ip.IPv4Network(lopool).hosts())]
	return loopbacks

def genIFaddress(ifpool):
    arr = []
    for addr in ip.ip_network(ifpool).subnets(new_prefix=31):
        ipaddr = list(ip.IPv4Network(addr).hosts())
        arr.append(ipaddr)
    return arr
    