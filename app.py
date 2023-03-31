from flask import Flask, request
import subprocess
import socket

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip_addr = request.form['ip_addr']

        # Validate the IP address before running the command
        try:
            socket.inet_aton(ip_addr)
        except socket.error:
            return 'Invalid IP address'

        # Run the shell command and capture the output
        command = 'coap-client -m get "coap://{}/temperature/meas1"'.format(ip_addr)
        try:
            result = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            return 'Error running command: {}'.format(str(e))

        # Output the result and add another input field and button for selecting another IP address
        return '''
            <div class="header">
              <h1>Temperature Measurement</h1>
            </div>
            <div class="content">
              <div class="result">
                <p>Result of the request:</p>
                <pre>{}</pre>
              </div>
              <div class="form">
                <form method="post">
                  <label for="ip_addr">Enter another IP address:</label>
                  <input type="text" id="ip_addr" name="ip_addr" required>
                  <button type="submit">Submit</button>
                </form>
              </div>
            </div>
        '''.format(result.decode())

    # If no form has been submitted yet, display the form
    return '''
        <div class="header">
          <h1>Temperature Measurement</h1>
        </div>
        <div class="content">
          <div class="form">
            <form method="post">
              <label for="ip_addr">Enter an IP address:</label>
              <input type="text" id="ip_addr" name="ip_addr" required>
              <button type="submit">Submit</button>
            </form>
          </div>
        </div>
    '''

# Link to the CSS file
@app.route('/static/style.css')
def css():
    return app.send_static_file('style.css')

if __name__ == '__main__':
    app.run()