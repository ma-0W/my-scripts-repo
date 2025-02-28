# ping localhost - select command based on os. 

# import necessary Python modules
import platform
import os

# Assign IP to ping to a variable
ip = "127.0.0.1"
# Determine the currrent OS
currrent_os = platform.system().lower()
# select ping command based on OS
if currrent_os == "windows":
    # ping command for Windows
    ping_cmd = f"ping -n 1 -w 2 {ip} > nul"
else:
    # ping command for Linux
    ping_cmd = f"ping -c 1 -w 2 {ip} > /dev/null 2>&1"

# Execute command and capture exit code
exit_code = os.system(ping_cmd)
# Print exit code - successful = 0
print(exit_code)
