#!/bin/bash
import sys
import subprocess
import time
import pandas as pd

# Function creating for ping
ip_list = []
mac_list = []
arguments=[]

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
    p = subprocess.Popen(f"ping -c 15 -s 52 {ip_list[x]}",shell=True,stdout=subprocess.PIPE)
    p.wait()
    if p.poll()==0:
        outage=1
    else:
        outage=0


def data():
    pd.options.display.max_rows = 50000
    df = pd.read_csv("/home/nick/Desktop/SSH For Linux/Rasp to WIndows(slave)/Server_Information.csv")
    for x in range(len(df)):
        ip_list.append(df.loc[x][0])
        mac_list.append(df.loc[x][2])

def ssh():
    p = subprocess.Popen(f'wakeonlan {mac_list[x]}',shell=True)
    
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
                if outage == 1:
                    print(f"{ip_list[x]} is UP")

                while outage == 0:
                    print(f"{ip_list[x]} is DOWN")
                    print(f"Trying to Wake Up {ip_list[x]}")
                    ssh()
                    print(
                        f"waiting 15 seconds before Pinging {ip_list[x]} again\n")
                    time.sleep(15)
                    ping_args()
                    attempt += 1
                    if attempt == 5:
                        print(f"\n{ip_list[x]} not Waking UP, Skipping\n")
                        break
                    elif outage==1:
                        print(f"{ip_list[x]} is UP")
if len(arguments) == 0:
    print("No Arguments were given, Waking all the available Servers")
    for x in range(len_list):
        attempt = 0
        # while Something to make script ping one address and if its down ping it again
        print(f"Pinging {ip_list[x]}")
        ping_args()
        if outage == 1:
            print(f"{ip_list[x]} is UP")

        while outage == 0:
            print(f"{ip_list[x]} is DOWN")
            print(f"Trying to Wake Up {ip_list[x]}")
            ssh()
            print(f"waiting 15 seconds before Pinging {ip_list[x]} again\n")
            time.sleep(15)
            ping_args()
            attempt += 1
            if attempt == 5:
                print(f"\n{ip_list[x]} not Waking UP, Skipping\n")
                break
            elif outage==1:
                print(f"{ip_list[x]} is UP")