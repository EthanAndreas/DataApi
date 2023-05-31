from utils import constant as const
from flask import Flask, request, render_template
from utils import function as func

app = Flask(__name__)

@app.route('/')
def home():
    """ Generate the home page
    """
    return render_template('home.html')

@app.route('/read', methods=['GET', 'POST'])
def read():
    """ Generate the read page where the user can enter an IP address and
    request the data from the sensor node
    """
    
    # If the user has entered an IP address, request the data
    if request.method == 'POST':
        ip_addr = request.form['ip_addr']
        result = func.request_pressure(ip_addr)

        return render_template('read.html', result=result, ip_addr=ip_addr)

    return render_template('read.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    """ Generate the test page where the user can enter multiple IP
    and their pressure value, and retrieve the calculated value
    """
    
    # If the user has entered an IP address, request the data
    if request.method == 'POST':
        num_addr = int(request.form['num_addr'])
        ip_addr = []
        pressure = []
        unit = []
        
        if num_addr > 0 and num_addr <= const.MAX_NUM_ADDR:
            for i in range(num_addr):
                ip_addr.append(request.form['ip_addr_' + str(i)])
                pressure.append(request.form['pressure_' + str(i)])
                unit.append(request.form['unit_' + str(i)])
        
            func.send_pressure(num_addr, ip_addr, pressure, unit)
            
            func.request_level(ip_addr[0])
        
    return render_template('test.html')


@app.context_processor
def inject_header_data():
    """ Inject the header data into the template
    """
    
    return {'pages': [
        {'href': '/', 'text': 'Home'},
        {'href': '/read', 'text': 'Read'},
        {'href': '/test', 'text': 'Simulate'}
    ]}

if __name__ == '__main__':
    app.run(debug=True)
