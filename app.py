from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/coap', methods=['POST'])
def coap():
    ip = request.form['ip']
    command = ['coap-client', '-m', 'get', 'coap://{}/temperature/meas1'.format(ip)]
    result = subprocess.check_output(command, stderr=subprocess.STDOUT)
    return result

if __name__ == '__main__':
    app.run(port=3000, debug=True)
