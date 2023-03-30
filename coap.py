#!/usr/bin/env python3

import cgi
import subprocess

# Read the IP address from the form
form = cgi.FieldStorage()
ip = form.getvalue("ip")

# Execute the coap-client command
command = ["coap-client", "-m", "get", "coap://{}/temperature/meas1".format(ip)]
result = subprocess.check_output(command, stderr=subprocess.STDOUT)

# Print the result as a HTML page
print("Content-Type: text/html")
print()
print("<!DOCTYPE html>")
print("<html>")
print("  <head>")
print("    <title>CoAP Client</title>")
print("  </head>")
print("  <body>")
print("    <h1>CoAP Client</h1>")
print("    <p>Result:</p>")
print("    <pre>{}</pre>".format(result.decode()))
print("  </body>")
print("</html>")
