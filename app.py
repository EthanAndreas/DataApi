import subprocess
import socket
import plotly.graph_objs as go
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'POST':
        ip_addr = request.form['ip_addr']

        # Validate the IP address before running the command
        try:
            socket.inet_aton(ip_addr)
        except socket.error:
            return 'Invalid IP address'

        # Check if the IP address is reachable
        response = subprocess.run(['ping', '-c', '0.5', ip_addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode != 0:
            return render_template('error.html', ip_addr=ip_addr)

        # Run the shell command and capture the output
        command = 'coap-client -m get "coap://{}/temperature/meas1"'.format(ip_addr)
        try:
            result = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            return 'Error running command: {}'.format(str(e))

        # Output the result and add another input field and button for selecting another IP address
        return render_template('recovery.html', result=result.decode(), ip_addr=ip_addr)

    # If no form has been submitted yet, display the form
    return render_template('recovery.html')

@app.route('/error')
def error():
    ip_addr = request.args.get('ip_addr')
    return render_template('error.html', ip_addr=ip_addr)

@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
    
    if request.method == 'POST':
        ip_addr = request.form['ip_addr']
    

    # Output the results
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
