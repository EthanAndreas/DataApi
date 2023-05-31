from utils import constant as const
import socket
import subprocess

def test_ip_addr(ip_addr):
    """ Test the IP address
    Args:
        str : IP address of the sensor node
    Returns:
        int : -4 if IP address is empty string, -3 if IP address is invalid,
        -2 if IP address is unreachable or 0 if the IP address is valid
    """

    # Test if IP address is empty
    if ip_addr == '':
        return const.NO_IP_ADDR
    
    # Test IP address format 
    parts = ip_addr.split('.')
    if len(parts) != 4:
        return const.INVALID_IP_ADDR
    for part in parts:
        if not part.isdigit():
            return const.INVALID_IP_ADDR
        num = int(part)
        if num < 0 or num > 255:
            return const.INVALID_IP_ADDR
        
    try:
        socket.inet_aton(ip_addr)
    except socket.error:
        return const.INVALID_IP_ADDR

    # Check if the IP address is on the network
    response = subprocess.run(['ping', '-c', '0.7', ip_addr], stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    if response.returncode != 0:
        return const.UNREACHABLE_IP_ADDR

    return const.SUCCESS

def request_pressure(ip_addr):
    """ Request the data from the IP address
    Args:
        str : IP address of the sensor node
    Returns:
        int : -4 if IP address is empty string, -3 if IP address is invalid, 
        -2 if IP address is unreachable, -1 if the command fails, or the 
        result of the command
    """
    
    # If the ip address is invalid, return the error code
    ret = test_ip_addr(ip_addr)
    if ret != const.SUCCESS:
        return ret
    
    # Run the shell command and capture the output
    # command = './bin/client {} value'.format(ip_addr)
    # try:
    #     result = subprocess.check_output(command, shell=True)
    # except subprocess.CalledProcessError as e:
    #     return const.FAILED_COMMAND

    # Output the result
    # return (int)(result.decode())

def request_configuration(ip_addr):
    """ Request the configuration from the IP address
    Args:
        str : IP address of the sensor node
    Returns:
        int : -4 if IP address is empty string, -3 if IP address is invalid, 
        -2 if IP address is unreachable, -1 if the command fails, or the 
        result of the command
    """
    
    # If the ip address is invalid, return the error code
    ret = test_ip_addr(ip_addr)
    if ret != const.SUCCESS:
        return ret
    
    # Run the shell command and capture the output
    # command = './bin/client {} conf'.format(ip_addr)
    # try:
    #     result = subprocess.check_output(command, shell=True)
    # except subprocess.CalledProcessError as e:
    #     return const.FAILED_COMMAND
    
def send_pressure(num_addr, ip_addr, pressure, unit):
    """ Send pressure values to the IP addresses
    Args:
        int : number of IP addresses
        list : list of IP addresses
        list : list of pressure values
        list : list of units
    """
    
    for i in range(num_addr):
        # If the ip address is invalid, return the error code
        ret = test_ip_addr(ip_addr[i])
        if ret != const.SUCCESS:
            return ret
        
        # Run the shell command and capture the output
        # command = './bin/server {} value pressure[i] unit[i]'.format(ip_addr)
        # try:
        #     result = subprocess.check_output(command, shell=True)
        # except subprocess.CalledProcessError as e:
        #     return const.FAILED_COMMAND
        
def request_level(ip_addr):
    """ Request the level calculated by the main device
    """
    
    output = request_configuration(ip_addr)
    
    # if the a line begins with 'main device' then retrieve the ip address
    # the format is 'main device : <ip address>'
    for line in output.splitlines():
        if line.startswith('main device'):
            main_device = line.split(':')[1].strip()
            
    # Run the shell command and capture the output
    # command = './bin/client {} level'.format(main_device)
    # try:
    #     result = subprocess.check_output(command, shell=True)
    # except subprocess.CalledProcessError as e:
    #     return const.FAILED_COMMAND 
    
    # Output the result
    # return (int)(result.decode())