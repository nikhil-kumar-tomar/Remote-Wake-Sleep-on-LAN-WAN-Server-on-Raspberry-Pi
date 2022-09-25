import paramiko

command = "/bin/python3 /home/pi/'SSH For Linux'/'Rasp to WIndows(slave)'/'Rasp_serv to Windows_slave(sleep).py' 0"
# Edit The "host", "username", "password" with your server information.

host = "192.168.196.153"
username = "pi"

client = paramiko.client.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username)
stdin, stdout,stderr = client.exec_command(command)

for line in stdout.readlines():
    lines=line.rstrip('\n')
    print(lines)
    if client:
        client.close()