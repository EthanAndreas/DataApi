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
    
    return -1
    
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
        
    return -1
        
def request_level(ip_addr):
    """ Request the level calculated by the main device
    args:
        list : list of ip addresses
    """
    
    # Take the first ip address to request the configuration
    output = request_configuration(ip_addr[0])
    if output != 0:
        return const.FAILED_REQUEST_CONF
    
    # Retrieve the ip address of the main device
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
    
def calculate_level(enter_ip_addr, enter_pressure, unit):
    """ Calculate the level from the pressure value
    args:
        list : list of ip addresses
        list : list of pressure values
    """
    
    # Take the first ip address to request the configuration
    output = request_configuration(enter_ip_addr[0])
    if output != 0:
        return const.FAILED_REQUEST_CONF
    
    # Retrieve the number of sensors
    for line in output.splitlines():
        if line.startswith('num sensors'):
            num_sensors = int(line.split(':')[1].strip())
            
    # Retrieve all the ip addresses
    ip_addr = [num_sensors]
    for line in output.splitlines() or line.startswith('secondary device'):
        if line.startswith('main device'):
            # Sort the ip addresses in function of their position
            ip = line.split(':')[1].strip()
            line = next(output)
            position = line.split(':')[1].strip()
            if position == 'top':
                ip_addr[-1] = ip
            elif position == 'bottom':
                ip_addr[0] = ip
            elif position == 'middle':
                ip_addr[1] = ip
                # Keep the height of the middle sensor
                line = next(output)
                height = float(line.split(':')[1].strip())
    
    # Convert the pressure values to the same unit in Pascal
    for i in range(num_sensors):
        if unit[i] == 'bar':
            enter_pressure[i] *= 100000
        elif unit[i] == 'psi':
            enter_pressure[i] *= 6894.76
    
    # Sort the pressure values in function of their ip address
    pressure = [num_sensors]
    for i in range(num_sensors):
        for j in range(num_sensors):
            if ip_addr[i] == enter_ip_addr[j]:
                pressure[i] = float(enter_pressure[j])
    
    if num_sensors == 1:
        # Note: the sensor should be at the bottom
        
        if gas_pressure == 'null' or density == 'null':
            return const.NO_GAS_PRESSURE_AND_DENSITY
        
        # Retrieve gas pressure and density
        for line in output.splitlines():
            if line.startswith('gas pressure'):
                gas_pressure = float(line.split(':')[1].strip())
            elif line.startswith('density'):
                density = float(line.split(':')[1].strip())
                
        # Calculate the level
        level = (pressure[0] - gas_pressure) / (density * 9.81)
        
    elif num_sensors == 2:
        # Note: the sensors should be at the top and bottom and the density should be known
        
        if gas_pressure == 'null':
            return const.NO_GAS_PRESSURE
        
        # Calculate the density
        density = (pressure[0] - pressure[1]) / (height * 9.81)
        level = (pressure[0] - gas_pressure) / (density * 9.81)
        
    elif num_sensors == 3:
        
        # Calculate the density
        density = (pressure[1] - pressure[2]) / (height * 9.81)
        level = (pressure[0] - pressure[2]) / (density * 9.81)
        
    return level
        
        
    
    