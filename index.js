const coap = require('coap');
const express = require('express');
const app = express();

// Define the style and background image constants
const style = 'style="width: 100%; font-family: "Gill Sans"; color:rgb(0,153,153); text-align: left;';

app.get('/', (req, res) => {

    res.write('<!DOCTYPE html>');
    res.write('<html>');
    res.write('<head>');
    res.write('<title>Data Retrieve API</title>');
    res.write('</head>');
    res.write('<body>');
    res.write('<div>');
    res.write('<h1> Retrieve the data on unknown IP address and print it with NodeJS</h1>');
    res.write('</div>');
    res.write('<div>');


    console.log('Request received');

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
                res.write(`<div ${style} style="margin-bottom: 10px;"><h2>Response from ${ip}:</h2><p>${data}</p></div>`);
            });
        }).end();
    }

    // Close the container div and the HTML tags
    res.write('</div>');
    res.write('</body>');
    res.write('</html>');

    // Send a response to the client
    res.end();
});


// Serve the background image
app.use('/assets', express.static('assets'));

// Start the server
app.listen(3000, () => {

    console.log('Server started on port 3000');
});
