import os
import socket
import sys
import threading
from queue import Queue
import time
from datetime import datetime
from colorama import init, Fore, Style
import subprocess
import requests
import json
import dns.resolver
import phonenumbers
from phonenumbers import geocoder
from opencage.geocoder import OpenCageGeocode

init(autoreset=True)
subprocess.call('clear', shell=True)

def maintool():
    target = input("ENTER TARGET IP:  ")
    ports = input("ENTER NUMBER OF PORTS TO SCAN:   ")
    threads = input("ENTER NUMBER OF THREADS (MAXIMUM: 3)   ")
    if threads == "1":
        thr = 1
    elif threads == "2":
        thr = 2
    elif threads == "3":
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
            worker = q.get()
            starthack(worker)
            q.task_done()

    q = Queue()

    for x in range(thr):
        t = threading.Thread(target=threader)
        t.daemon = False
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
            if result == 0:
                service = socket.getservbyport(port)

                print("-----------------------------------------")
                print(Style.BRIGHT + Fore.YELLOW + "PORT:", port, Style.BRIGHT + Fore.GREEN + "    OPEN")
                print(Style.BRIGHT + Fore.YELLOW + "INFORMATION")
                print(service)
                print("-----------------------------------------")
                hacking.close()

                print("")
                print("")
                if port == 21:
                    print("FTP IS OPEN!! ")
                    print("CHECKING FOR ANONYMOUS AUTHENTICATION")
                    with open('FTPTarget.txt', 'w') as st:
                        st.write(hack)
                        st.close()
                    os.system("xterm -e 'python3 ftp.py'")

                if port == 22:
                    print("SSH IS OPEN!!")
                    print("ATTEMPTING BRUTEFORCE ATTACK")
                    with open('SSHTarget.txt', 'w') as st:
                        st.write(hack)
                        st.close()
                    os.system("xterm -e 'proxychains python3 attack.py'")




            else:
                print("-----------------------------------------")
                print(Style.BRIGHT + Fore.YELLOW + "PORT:", port, Style.BRIGHT + Fore.RED + "    CLOSED")
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


def mainmenu():
    print(Style.BRIGHT + Fore.YELLOW + "START AT:", (datetime.now()))
    print("=============COREXITAL MULTITOOL=============")
    print("")
    print("Written by: Derek Johnston")
    print('\n',
    "Get IP location [1] \n",
    "Get DNS information [2] \n",
    "Port scan with automatic FTP Anon login and automatic SSH brute [3] \n",
    "Get location of phone number [4] \n"
    )
    todo = input(Style.BRIGHT + Fore.YELLOW + "Select Options:    ")
    if todo == "1":
        geotar()
    elif todo == "2":
        dnsloc()
    elif todo == "3":
        maintool()
    elif todo =="4":
        phonloc()
    else:
        print("Invalid Input!!! Quitting!!")
        sys.exit()


def phonloc():
    numenter = input(Style.BRIGHT + Fore.YELLOW + "Enter phone number with country code (+1 US/CA)")
    print(numenter)
    pepnumber = phonenumbers.parse(numenter.get())
    location = phonenumbers.geocoder.description_for_number(pepnumber, "en")

    print("LOCATION:")
    print(location)

    key = '7b5057c5d0594b948600eaf3affa261d'

    geocoder = OpenCageGeocode(key)
    query = str(location)
    results = geocoder.geocode(query)

    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']
    print("GPS COORDINATES:")
    print(lat, lng)
    print("END OF REPORT")
    print("Corexital Data 2023")
    enterex = input(Style.BRIGHT + Fore.YELLOW + "Select '1' to return to main menu \n or '2' to quit")
    if enterex == "1":
        mainmenu()
    elif enterex == "2":
        sys.exit()
    else:
        print("Invalid Input!!! Returning to main menu")
        mainmenu()
def geotar():
    GeoTar = input(Style.BRIGHT + Fore.YELLOW + "Enter IP:  ")
    print(Style.BRIGHT + Fore.YELLOW + "Getting IP Location.....")
    request_url = 'https://geolocation-db.com/jsonp/' + GeoTar
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result = json.loads(result)
    print(result)
    time.sleep(2)
    enterex = input(Style.BRIGHT + Fore.YELLOW + "Select '1' to return to main menu \n or '2' to quit")
    if enterex == "1":
        mainmenu()
    elif enterex == "2":
        sys.exit()
    else:
        print("Invalid Input!!! Returning to main menu")
        mainmenu()

def dnsloc():
    dnstar = input(Style.BRIGHT + Fore.YELLOW + "Enter host name:  ")
    dnsinfo: dns.resolver.Answer = dns.resolver.resolve(dnstar)
    print(Style.BRIGHT + Fore.BLUE + 'query qname:', dnsinfo.qname,  len(dnsinfo))
    for rdata in dnsinfo:
        print(rdata)
    dnsinfo: dns.resolver.Answer = dns.resolver.resolve(dnstar, 'MX')
    for rdata in dnsinfo:
        print(Style.BRIGHT + Fore.BLUE + "MX: ")
        print(rdata)
    dnsinfo: dns.resolver.Answer = dns.resolver.resolve(dnstar, 'NS')
    for rdata in dnsinfo:
        print(Style.BRIGHT + Fore.BLUE + "NAMESERVERS: ")
        print(rdata)
    dnsinfo: dns.resolver.Answer = dns.resolver.resolve(dnstar, 'TXT')
    for rdata in dnsinfo:
        print(Style.BRIGHT + Fore.BLUE + "TXT RECORDS: ")
        print(rdata)

    time.sleep(2)
    enterexdns = input(Style.BRIGHT + Fore.YELLOW + "Press '1' to return to main menu. Press '2' to exit")
    if enterexdns == '1':
        mainmenu()
    elif enterexdns == '2':
        print("Quitting")
        sys.exit()
    else:
        print("Invalid Input!!! Returning to main menu")
        mainmenu()



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

print("Proxychains")
time.sleep(1)
check_prx = subprocess.run(["which", "proxychains"], capture_output=True, text=True)
if "proxychains" in check_prx.stdout:
    print("Proxychains is Installed")
else:
    install_prx = subprocess.run(["sudo", "apt", "install", "proxychains", "-y"], capture_output=True, text=True)
    if "Setting up Proxychains" in install_prx.stdout:
        print("\n[*] Proxychains Installed")

    else:
        print("Install Proxychains manually!!!!")
        print("sudo apt install proxychains")
        time.sleep(1.5)
        sys.exit()
time.sleep(1)


print("REQUIREMENTS")
os.system('pip install -r requirements.txt')
os.system('cls' if os.name == 'nt' else 'clear')
mainmenu()


