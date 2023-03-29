const coap = require('coap');
const express = require('express');
const app = express();

// Endpoint to handle CoAP requests and display the response on a webpage
app.get('/', (req, res) => {
    // Set the title of the webpage
    res.write('<html><head><title>Retrieve the data on unknown IP address and print it with NodeJS</title></head><body>');

    // Iterate through IP addresses between 10.0.0.5 and 10.0.0.254
    for (let i = 5; i <= 254; i++) {
        const ip = `10.0.0.${i}`;

        // Send a CoAP request to the current IP address
        coap.request(`coap://${ip}`, 'GET').on('response', coapRes => {
            let data = '';
            coapRes.on('data', chunk => {
                data += chunk.toString();
            });
            coapRes.on('end', () => {
                console.log(`Response from ${ip}: ${data}`);
                // Display the response on the webpage
                res.write(`<div style="margin-bottom: 10px;"><h2>Response from ${ip}:</h2><p>${data}</p></div>`);
            });
        }).end();
    }

    // Close the HTML tags
    res.write('</body></html>');

    // Send a response to the client
    res.end();
});

// Start the server
app.listen(3000, () => {
    console.log('Server started on port 3000');
});
