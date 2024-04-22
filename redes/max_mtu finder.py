import os
import subprocess

def find_max_mtu(target):
    """
    Finds the maximum MTU size that doesn't fragment packets to the specified target.
    
    Args:
    target (str): The target host to test MTU sizes against.
    
    Returns:
    int: The maximum MTU size.
    """
    min_mtu = 1450   # Minimum reasonable MTU size
    max_mtu = 1900  # Maximum standard MTU size for Ethernet
    max_working_mtu = min_mtu  # Largest MTU size tested that doesn't fragment packets

    for mtu in range(min_mtu, max_mtu + 1):
        # The '-M do' option prevents fragmentation
        # The '-s' option sets the size of the packet, which we set to the current MTU being tested
        # We subtract 28 because 20 bytes are reserved for the IP header and 8 bytes for the ICMP header
        response = subprocess.run(['ping', '-M', 'do', '-c', '1', '-s', str(mtu - 28), target], 
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        if "Frag needed" not in str(response.stdout):
            max_working_mtu = mtu
        else:
            break

    return max_working_mtu

# Example usage
target_host = "189.90.15.106"  # Replace with the desired target host
max_mtu = find_max_mtu(target_host)
print(f"Maximum MTU size to {target_host}: {max_mtu}")
