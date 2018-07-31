import ipaddress as ip
import jinja2

pool = '192.168.10.0/24'
ifl = '0'  #unit number
iface = ''  #interface ip pool

loopbacks = [ str(x) for x in (ip.IPv4Network(pool).hosts())]






