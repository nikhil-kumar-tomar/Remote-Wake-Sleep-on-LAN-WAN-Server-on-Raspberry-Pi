import sys
import subprocess
import time
import paramiko
import pandas as pd
import os

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Server_Information.csv")
df = pd.read_csv(filename)
arguments = []
err=0
def args():
    args = sys.argv
    for len_args in range(1, len(args)):
        arguments.append(int(args[len_args]))

# p.poll() = 0 means servers are Up and running
# p.poll() = 1 means servers are Down and must be wake up.
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

def ssh(ip_address,user_name):
    global err
    try:       
        command = "rundll32.exe powrprof.dll, SetSuspendState Sleep"

        host = f"{ip_address}"
        username = f"{user_name}"

        client = paramiko.client.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username)
        stdin, stdout,stderr = client.exec_command(command)
        client.close()
    except Exception as error:
        err=error

args()
if len(arguments) != 0:
    for l in arguments:
        ip_address=df["IP_Address"][l]
        user_name=df["SSH_Users"][l]
        attempt = 0
        # while Something to make script ping one address and if its down ping it again
        print(f"Pinging {ip_address}")
        ping_args(ip_address)
        if outage == 0:
            print(f"{ip_address} is DOWN")

        while outage == 1:
            print(f"{ip_address} is UP")
            print(f"Trying to put {ip_address} to SLEEP")
            ssh(ip_address,user_name)
            print(f"waiting 15 seconds before Pinging {ip_address} again\n")
            time.sleep(15)
            ping_args(ip_address)
            if attempt == 5 or err!=0:
                if err!=0:
                    if "[Errno 110] Connection timed out" in str(err):
                        print("Connection timed out, Your server is non responsive")
                    elif ("No Authentication Methods available" in str(err)) or ("Authentication failed" in str(err)):
                        print(f"Authentication Failed, Private/Public keys might not be configured for {ip_address}")
                    else:
                        print(err)
                print(f"\n{ip_address} not going to Sleep, Skipping\n")
                break
            elif outage==0:
                print(f"{ip_address} is DOWN")
            attempt += 1

elif len(arguments) == 0:
    print("No Arguments were given, Putting all the available Servers to Sleep")
    for x in range(len(df)):
        ip_address=df['IP_Address'][x]
        user_name=df["SSH_Users"][x]
        attempt = 0
        # while Something to make script ping one address and if its down ping it again
        print(f"Pinging {ip_address}")
        ping_args(ip_address)
        if outage == 0:
            print(f"{ip_address} is DOWN")
        while outage == 1:
            print(f"{ip_address} is UP")
            print(f"Trying to put {ip_address} to SLEEP")
            ssh(ip_address,user_name)
            print(f"waiting 15 seconds before Pinging {ip_address} again\n")
            time.sleep(15)
            ping_args(ip_address)
            if attempt == 5 or err!=0:
                if err!=0:
                    if "[Errno 110] Connection timed out" in str(err):
                        print("Connection timed out, Your server is non responsive")
                    elif ("No Authentication Methods available" in str(err)) or ("Authentication failed" in str(err)):
                        print(f"Authentication Failed, Private/Public keys might not be configured for {ip_address}")
                    else:
                        print(err)
                
                print(f"\n{ip_address} not going to Sleep, Skipping\n")
                break
            elif outage==0:
                print(f"{ip_address} is DOWN")
            attempt += 1
