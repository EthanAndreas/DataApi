import subprocess
import socket
import plotly.graph_objs as go
from flask import Flask, request, render_template

app = Flask(__name__)

import socket
import subprocess

def request_ip_addr(ip_addr):
    
    # Test if IP address is empty
    if ip_addr == '':
        return -2
    
    # Test IP address format 
    parts = ip_addr.split('.')
    if len(parts) != 4:
        return -1
    for part in parts:
        if not part.isdigit():
            return -1
        num = int(part)
        if num < 0 or num > 255:
            return -1

    # Validate the IP address before running the command
    try:
        socket.inet_aton(ip_addr)
    except socket.error:
        return -1

    # Check if the IP address is reachable
    response = subprocess.run(['ping', '-c', '0.7', ip_addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode != 0:
        return -1

    # Run the shell command and capture the output
    command = 'coap-client -m get "coap://{}/temperature/meas1"'.format(ip_addr)
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        return -1

    # Output the result
    return result.decode()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'POST':
        ip_addr = request.form['ip_addr']
        result = request_ip_addr(ip_addr)

        return render_template('recovery.html', result=result, ip_addr=ip_addr)

    return render_template('recovery.html')

@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
    
    if request.method == 'POST':
        num_addr = int(request.form['num_addr'])
        ip_addr = []
        result = []
        
        if num_addr == 1:
            ip_addr.append(request.form['ip_addr_1'])
            result.append(request_ip_addr(ip_addr[0]))
            
        elif num_addr == 2:
            ip_addr.append(request.form['ip_addr_1'])
            ip_addr.append(request.form['ip_addr_2'])
            result.append(request_ip_addr(ip_addr[0]))
            result.append(request_ip_addr(ip_addr[1]))
            
        else:
            ip_addr.append(request.form['ip_addr_1'])
            ip_addr.append(request.form['ip_addr_2'])
            ip_addr.append(request.form['ip_addr_3'])
            result.append(request_ip_addr(ip_addr[0]))
            result.append(request_ip_addr(ip_addr[1]))
            result.append(request_ip_addr(ip_addr[2]))
            
        return render_template('simulation.html', ip_addr=ip_addr, result=result, num_addr=num_addr)
    
    return render_template('simulation.html')


@app.context_processor
def inject_header_data():
    return {'pages': [
        {'href': '/', 'text': 'Home'},
        {'href': '/recovery', 'text': 'Recovery'},
        {'href': '/simulation', 'text': 'Simulation'}
    ]}

if __name__ == '__main__':
    app.run(debug=True)
