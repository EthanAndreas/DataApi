from src.config import constant as const
from flask import Flask, request, render_template
from src import function as func

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
        result = func.request_ip_addr(ip_addr)

        return render_template('read.html', result=result, ip_addr=ip_addr)

    return render_template('read.html')

@app.route('/simulation', methods=['GET', 'POST'])
def simulation():
    """ Generate the simulation page where the user can enter multiple IP
    and calculate precise value with the data from the sensor nodes
    """
    
    # Initialize the value variable before the others variables
    # because if the user has not entered an IP address, the value
    # cannot be calculated whereas it is used in the template
    value = const.NO_VALUE
    
    # If the user has entered an IP address, request the data
    if request.method == 'POST':
        num_addr = int(request.form['num_addr'])
        ip_addr = []
        result = []
        
        if num_addr == 1:
            ip_addr.append(request.form['ip_addr_1'])
            result.append(func.request_ip_addr(ip_addr[0]))
            
            # Calculate the precise value
            if (result[0] >= 0):
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=func.calculate_fluid_level(num_addr, result))
            
        elif num_addr == 2:
            ip_addr.append(request.form['ip_addr_1'])
            ip_addr.append(request.form['ip_addr_2'])
            result.append(func.request_ip_addr(ip_addr[0]))
            result.append(func.request_ip_addr(ip_addr[1]))
            
            # Calculate the precise value
            if (result[0] >= 0 and result[1] >= 0):
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=func.calculate_fluid_level(num_addr, result))
                
            if (result[0] >= 0 and result[1] == -4):
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=func.calculate_fluid_level(1, result))
            
        else:
            ip_addr.append(request.form['ip_addr_1'])
            ip_addr.append(request.form['ip_addr_2'])
            ip_addr.append(request.form['ip_addr_3'])
            result.append(func.request_ip_addr(ip_addr[0]))
            result.append(func.request_ip_addr(ip_addr[1]))
            result.append(func.request_ip_addr(ip_addr[2]))
            
            # Calculate the precise value
            if (result[0] >= 0 and result[1] >= 0 and result[2] >= 0):
                return render_template('simulation.html', ip_addr=ip_addr, 
                                       result=result, num_addr=num_addr, 
                                       value=func.calculate_fluid_level(num_addr, result))
            
        return render_template('simulation.html', ip_addr=ip_addr, result=result, 
                               value=value, num_addr=num_addr)
    
    return render_template('simulation.html', value=value)


@app.context_processor
def inject_header_data():
    """ Inject the header data into the template
    """
    
    return {'pages': [
        {'href': '/', 'text': 'Home'},
        {'href': '/read', 'text': 'Read'},
        {'href': '/simulation', 'text': 'Simulate'}
    ]}

if __name__ == '__main__':
    app.run(debug=True)
