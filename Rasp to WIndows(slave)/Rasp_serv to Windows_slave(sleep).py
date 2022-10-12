#!/bin/bash
import sys
import subprocess
import time
import paramiko
import pandas as pd
# Function creating for ping
ip_list = []
mac_list = []
arguments = []
user_list=[]


def args():
    args = sys.argv
    length = len(args)
    for len_args in range(1, length, 1):
        arguments.append(int(args[len_args]))

# p.poll() = 0 means servers are Up and running
# p.poll() = 1 means servers are Down and must be wake up.
#outage =1 is up
#outage =0 is down


def ping_args():
    global outage
    p = subprocess.Popen(
        f"ping -c 15 -s 52 {ip_list[x]}", shell=True, stdout=subprocess.PIPE)
    p.wait()
    if p.poll() == 0:
        outage = 1
    else:
        outage = 0


def data():
    pd.options.display.max_rows = 50000
    df = pd.read_csv("/home/pi/SSH For Linux/Rasp to WIndows(slave)/Server_Information.csv")
    mac_list.extend(df['Mac_Address'].tolist())
    ip_list.extend(df["IP_Address"].tolist())
    user_list.extend(df["SSH_Users"].tolist())

def ssh():

    try:        
        command = "rundll32.exe powrprof.dll, SetSuspendState Sleep"


        host = f"{ip_list[x]}"
        username = f"{user_list[x]}"

        client = paramiko.client.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username)
        stdin, stdout,stderr = client.exec_command(command)
        client.close()
    except paramiko.ssh_exception.NoValidConnectionsError or paramiko.ssh_exception.AuthenticationException:
        something=f"Not able to connect to openssh server on port 22 on {ip_list[x]}"
        return(something)    
    


data()
args()
len_list = len(ip_list)
if len(arguments) != 0:
    for x in range(len_list):
        for l in arguments:
            if int(x) == int(l):
                attempt = 0
                # while Something to make script ping one address and if its down ping it again
                print(f"Pinging {ip_list[x]}")
                ping_args()
                if outage == 0:
                    print(f"{ip_list[x]} is DOWN")

                while outage == 1:
                    print(f"{ip_list[x]} is UP")
                    print(f"Trying to put {ip_list[x]} to SLEEP")
                    ssh()
                    print(
                        f"waiting 15 seconds before Pinging {ip_list[x]} again\n")
                    time.sleep(15)
                    ping_args()
                    attempt += 1
                    if attempt == 5:
                        print(f"\n{ip_list[x]} not going to Sleep, Skipping\n")
                        break
                    elif outage==0:
                        print(f"{ip_list[x]} is DOWN")
if len(arguments) == 0:
    print("No Arguments were given, Putting all the available Servers to Sleep")
    for x in range(len_list):
        attempt = 0
        # while Something to make script ping one address and if its down ping it again
        print(f"Pinging {ip_list[x]}")
        ping_args()
        if outage == 0:
            print(f"{ip_list[x]} is DOWN")

        while outage == 1:
            print(f"{ip_list[x]} is UP")
            print(f"Trying to put {ip_list[x]} to SLEEP")
            ssh()
            print(f"waiting 15 seconds before Pinging {ip_list[x]} again\n")
            time.sleep(15)
            ping_args()
            attempt += 1
            if attempt == 5:
                print(f"\n{ip_list[x]} not going to Sleep, Skipping\n")
                break
            elif outage==0:
                print(f"{ip_list[x]} is DOWN")