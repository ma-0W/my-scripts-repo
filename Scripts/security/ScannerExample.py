# Port scanner 
#'pip3 install python-nmap'

import nmap

# Identify target address
# The /24 means that the scan will cover all addresses in the subnet 
target_addresses = "192.168.1.0/24"

# Identify the ports for the scan
ports = "1-100"

# Create the scanner object
scanner = nmap.PortScanner()

# Scan the network
results = scanner.scan(target_addresses, ports, arguments="-T5")

# Report results
for target, host in results['scan'].items():
    print(target)

    # If open ports are found, print the current state
    if 'tcp' in host:
        for port, status in host['tcp'].items():
            print(f"\t{port} - {status['state']} ({status['name']})")
