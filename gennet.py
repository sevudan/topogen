import ipaddress as ip

pool = '192.168.10.0/24'

def genLoopback(pool='192.168.10.0/24'):
	loopbacks = [str(x) for x in (ip.IPv4Network(pool).hosts())]
	return loopbacks

def genIfaddress(pool='10.250.0.0/23'):
    loopbacks = [str(x) for x in (ip.IPv4Network(pool).hosts())]
    return loopbacks