#!/bin/bash
import sys
import subprocess
import time
import pandas as pd
import os

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Server_Information.csv")
df = pd.read_csv(filename)
arguments=[]

def args():
    args = sys.argv
    length = len(args)
    for len_args in range(1, length, 1):
        arguments.append(int(args[len_args]))

# p.poll() = 0 means servers are Up and running
# p.poll() = 1 or any other value means servers are Down and must be wake up.
#outage =1 is up
#outage =0 is down

def ping_args(ip_address):
    global outage
    p = subprocess.Popen(
        f"ping -c 15 -s 52 {ip_address}", shell=True, stdout=subprocess.PIPE)
    p.wait()
    if p.poll() == 0:
        outage = 1
    else:
        outage = 0


def ssh(mac_address):
    p = subprocess.Popen(f'wakeonlan {mac_address}',shell=True)
    
args()
if len(arguments) != 0:
    for l in arguments:
        ip_address=df["IP_Address"][l]
        mac_address=df["Mac_Address"][l]
        attempt = 0
        print(f"Pinging {ip_address}")
        ping_args(ip_address)
        if outage == 1:
            print(f"{ip_address} is UP")

        while outage == 0:
            print(f"{ip_address} is DOWN")
            print(f"Trying to Wake Up {ip_address}")
            ssh(mac_address)
            print(f"waiting 15 seconds before Pinging {ip_address} again\n")
            time.sleep(15)
            ping_args(ip_address)
            if attempt == 5:
                print(f"\n{ip_address} not Waking UP, Skipping\n")
                break
            elif outage==1:
                print(f"{ip_address} is UP")
            attempt += 1

elif len(arguments) == 0:
    print("No Arguments were given, Waking all the available Servers")
    for x in range(len(df)):
        ip_address=df["IP_Address"][x]
        mac_address=df["Mac_Address"][x]
        attempt = 0
        print(f"Pinging {ip_address}")
        ping_args(ip_address)
        if outage == 1:
            print(f"{ip_address} is UP")

        while outage == 0:
            print(f"{ip_address} is DOWN")
            print(f"Trying to Wake Up {ip_address}")
            ssh(mac_address)
            print(f"waiting 15 seconds before Pinging {ip_address} again\n")
            time.sleep(15)
            ping_args(ip_address)
            if attempt == 5:
                print(f"\n{ip_address} not Waking UP, Skipping\n")
                break
            elif outage==1:
                print(f"{ip_address} is UP")
            attempt += 1