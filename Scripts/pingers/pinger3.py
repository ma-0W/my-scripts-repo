import platform
import os
import time
import sys

""" 
pings a range of IP addresses (from 192.168.0.1 to 192.168.0.254) and prints which ones are online.
"""


# ip prefix to begin pinging
ip_prefix = "192.168.1."
# Determine the currrent OS
current_os = platform.system().lower()


# Loop from 0 - 254
for final_octet in range(254):
    # Adding 1 to final_octet to cycle through octet range 
    ip = ip_prefix + str(final_octet + 1)
    if current_os == "windows":
        # Build our ping command for Windows
        ping_cmd = f"ping -n 1 -w 500 {ip} > nul"
    else:
        # Build our ping command for other OSs
        ping_cmd = f"ping -c 1 -w 2 {ip} > /dev/null 2>&1"

    # Print progress using spinner
    print(f"Pinging {ip}...\n", end=" ")

    # Execute command and capture exit code
    exit_code = os.system(ping_cmd)
    # Print online if exit code = 0, successful ping 
    if exit_code == 0:
        print("{0} is online".format(ip))
    else:
        print("no response")
