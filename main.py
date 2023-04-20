import os
import socket
import sys
import threading
from queue import Queue
import time
from datetime import datetime
from colorama import init, Fore, Style
import subprocess

init(autoreset=True)
subprocess.call('clear', shell=True)


print("Checking For Dependencies.....")
time.sleep(1)
print("XTerm")
time.sleep(1)
check_xterm = subprocess.run(["which", "xterm"], capture_output=True, text=True)
if "xterm" in check_xterm.stdout:
    print("XTerm is Installed")
else:
    install_xterm = subprocess.run(["sudo", "apt", "install", "xterm", "-y"], capture_output=True, text=True)
    if "Setting up xterm" in install_xterm.stdout:
        print("\n[*] Xterm Installed")

    else:
        print("Install Xterm manually!!!!")
        print("sudo apt install xterm")
        time.sleep(1.5)
        sys.exit()
time.sleep(1)
print("REQUIREMENTS")
os.system('pip install -r requirements.txt')
os.system('cls' if os.name == 'nt' else 'clear')
print(Style.BRIGHT + Fore.YELLOW + "START AT:", (datetime.now()))
print("=============COREXITAL PORT SCANNER=============")
print("")
print("Written by: Derek Johnston")
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

num = int(ports)
print("Starting at: ")

t1 = datetime.now()
print(t1)
###################################################################################################
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



print(Style.BRIGHT + Fore.YELLOW + "SCANNING:", target)
print("WAITING FOR RESULTS...")
#################################################################################################
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
                    with open('FTPTarget.txt', 'w') as st:
                        st.write(hack)
                        st.close()
                    os.system("xterm -e 'python3 ftp.py'")

                if port ==22:
                    print("SSH IS OPEN!!")
                    print("ATTEMPTING BRUTEFORCE ATTACK")
                    with open('SSHTarget.txt', 'w') as st:
                        st.write(hack)
                        st.close()
                    os.system("xterm -e 'proxychains python3 attack.py'")




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



# 10 jobs assigned.
for worker in range(1, num):
    q.put(worker)

# wait till the thread terminates.
q.join()
print("FINISHED SCANNING TARGET:", target)
os.system('date')
print(Style.BRIGHT + Fore.YELLOW + "END OF REPORT")
print("2023 - Corexital")
