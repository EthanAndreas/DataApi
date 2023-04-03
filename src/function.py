from src.config import constant as const
import socket
import subprocess

def request_ip_addr(ip_addr):
    """ Request the data from the IP address
    Args:
        str : IP address of the sensor node
    Returns:
        int : -4 if IP address is empty string, -3 if IP address is invalid, 
        -2 if IP address is unreachable, -1 if the command fails, or the 
        result of the command
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

    # Run the shell command and capture the output
    command = 'coap-client -m get "coap://{}/temperature/meas1"'.format(ip_addr)
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        return const.FAILED_COMMAND

    # Output the result
    return (int)(result.decode())

def calculate_fluid_level(num_addr, result):
    """ Calculate the fluid's level in the tank from the data from the sensor 
    nodes, the pressure value are differenciate by their value and the tank
    measures 3 meters high and if there is a third sensor node, it is placed
    at the half of the tank
    
    Args:
        int : number of sensor nodes
        list : list of the pressure values (in Pa) from the sensor nodes
        
    Returns:
        float : the precise value
    """
    
    # TODO: in the data packet, there is the value and the id of the sensor node
    # differentiate the value by the id of the sensor node 
    
    value = const.NO_VALUE
    
    if num_addr == 1:
        # Fix density of the fluid to 1000 kg/m^3 and the gas pressure to 101325 Pa
        value = (result[0] - 101325) / (1000 * 9.81)
    
    if num_addr == 2:
        # Fix density of the fluid to 1000 kg/m^3
        if result[0] > result[1]:
            value = (result[0] - result[1]) / (1000 * 9.81)
        else:
            value = (result[0] - result[1]) / (1000 * 9.81)
    
    if num_addr == 3:
        # Calculate the density of the fluid
        if result[0] > result[1] and result[0] > result[2] and result[1] > result[2]:
            density = (result[0] - result[1]) / (9.81 * 1.5)
            value = (result[0] - result[2]) / (density * 9.81)
        elif result[0] > result[1] and result[0] > result[2] and result[2] > result[1]:
            density = (result[0] - result[2]) / (9.81 * 1.5)
            value = (result[0] - result[1]) / (density * 9.81)
        
        elif result[1] > result[0] and result[1] > result[2] and result[0] > result[2]:
            density = (result[1] - result[0]) / (9.81 * 1.5)
            value = (result[1] - result[2]) / (density * 9.81)
        elif result[1] > result[0] and result[1] > result[2] and result[2] > result[0]:
            density = (result[1] - result[2]) / (9.81 * 1.5)
            value = (result[1] - result[0]) / (density * 9.81)
        
        elif result[2] > result[0] and result[2] > result[1] and result[0] > result[1]:
            density = (result[2] - result[0]) / (9.81 * 1.5)
            value = (result[2] - result[1]) / (density * 9.81)
        elif result[2] > result[0] and result[2] > result[1] and result[1] > result[0]:
            density = (result[2] - result[1]) / (9.81 * 1.5)
            value = (result[2] - result[0]) / (density * 9.81)
    
    if (value < 0 or value > 3):
        return const.OUT_OF_RANGE

    return round(value,1)