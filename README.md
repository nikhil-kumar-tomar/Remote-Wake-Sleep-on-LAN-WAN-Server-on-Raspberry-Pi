
# Remote-Wake/Sleep-on-LAN-WAN-Server-on-Raspberry-Pi


This program allows you to wake/sleep your servers on LAN, it is supposed to be run in Raspberry Pi on Raspberry pi OS.

It works a little differently then what other scripts are out there. The way this script works is on demand for waking a specific server it takes the servers mac address and sends a wake on lan magic packet to it, for making the server go to sleep it ssh's into the machine and run the command for sleeping, for security reasons I have to remove the password from the script.

Therefore if the script wants to ssh into the computer it uses private/public keys for that purpose instead of the old password. This means whosoever is installing this should have to configure public/private ssh keys on the server and raspberry pi.

The biggest need for this script was to make the server actually go to sleep on command, since many scripts I tried failed to do that exact purpose.

As, I said the script is currently in Development so i was not able to insert Installation guide but I will do that in the future.


