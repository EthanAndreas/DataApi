import subprocess
import socket
from flask import Flask, request, render_template

app = Flask(__name__)

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
        return -4
    
    # Test IP address format 
    parts = ip_addr.split('.')
    if len(parts) != 4:
        return -3
    for part in parts:
        if not part.isdigit():
            return -3
        num = int(part)
        if num < 0 or num > 255:
            return -3
        
    try:
        socket.inet_aton(ip_addr)
    except socket.error:
        return -3

    # Check if the IP address is on the network
    response = subprocess.run(['ping', '-c', '0.7', ip_addr], stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    if response.returncode != 0:
        return -2

    # Run the shell command and capture the output
    command = 'coap-client -m get "coap://{}/temperature/meas1"'.format(ip_addr)
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        return -1

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
    
    value = -1
    
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
        return -2

    return value

@app.route('/')
def home():
    """ Generate the home page
    """
    return render_template('home.html')

@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    """ Generate the recovery page where the user can enter an IP address and
    request the data from the sensor node
    """
    
    # If the user has entered an IP address, request the data
    if request.method == 'POST':
        ip_addr = request.form['ip_addr']
        result = request_ip_addr(ip_addr)

        return render_template('recovery.html', result=result, ip_addr=ip_addr)

    return render_template('recovery.html')

@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
    """ Generate the simulation page where the user can enter multiple IP
    and calculate precise value with the data from the sensor nodes
    """
    
    # Initialize the value variable before the others variables
    # because if the user has not entered an IP address, the value
    # cannot be calculated whereas it is used in the template
    value = -1
    
    # If the user has entered an IP address, request the data
    if request.method == 'POST':
        num_addr = int(request.form['num_addr'])
        ip_addr = []
        result = []
        
        if num_addr == 1:
            ip_addr.append(request.form['ip_addr_1'])
            result.append(request_ip_addr(ip_addr[0]))
            
            # Calculate the precise value
            if (result[0] >= 0):
                value = round(calculate_fluid_level(num_addr, result),1)
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=value)
            
        elif num_addr == 2:
            ip_addr.append(request.form['ip_addr_1'])
            ip_addr.append(request.form['ip_addr_2'])
            result.append(request_ip_addr(ip_addr[0]))
            result.append(request_ip_addr(ip_addr[1]))
            
            # Calculate the precise value
            if (result[0] >= 0 and result[1] >= 0):
                value = round(calculate_fluid_level(num_addr, result),1)
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=value)
                
            if (result[0] >= 0 and result[1] == -4):
                value = round(calculate_fluid_level(1, result),1)
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=value)
            
        else:
            ip_addr.append(request.form['ip_addr_1'])
            ip_addr.append(request.form['ip_addr_2'])
            ip_addr.append(request.form['ip_addr_3'])
            result.append(request_ip_addr(ip_addr[0]))
            result.append(request_ip_addr(ip_addr[1]))
            result.append(request_ip_addr(ip_addr[2]))
            
            result[0] = 101326
            result[2] = 101326
            result[1] = 101326
            
            # Calculate the precise value
            if (result[0] >= 0 and result[1] >= 0 and result[2] >= 0):
                value = round(calculate_fluid_level(num_addr, result),1)
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=value)
            
        return render_template('simulation.html', ip_addr=ip_addr, result=result, 
                               value=value, num_addr=num_addr)
    
    return render_template('simulation.html', value=value)


@app.context_processor
def inject_header_data():
    """ Inject the header data into the template
    """
    
    return {'pages': [
        {'href': '/', 'text': 'Home'},
        {'href': '/recovery', 'text': 'Recovery'},
        {'href': '/simulation', 'text': 'Simulation'}
    ]}

if __name__ == '__main__':
    app.run(debug=True)
