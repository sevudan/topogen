import ipaddress as ip

pool = '192.168.10.0/24'

def genLoopback(pool='192.168.10.0/24'):
	loopbacks = [str(x) for x in (ip.IPv4Network(pool).hosts())]
	return loopbacks
	