import os
import subprocess
import time
import sys



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
