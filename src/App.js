import React, { useState, useEffect } from "react";
import coap from "coap";

const App = () => {
    const [data, setData] = useState([]);

    const title = "Retrieve data on unknown IP addresses";

    useEffect(() => {
        const fetchData = async () => {
            const validIPs = [];

            for (let i = 5; i <= 254; i++) {
                const ip = `10.0.0.${i}`;
                try {
                    const req = coap.request(`coap://${ip}`);
                    req.on('response', (res) => {
                        if (res.code === '2.05') {
                            validIPs.push(ip);
                        } else {
                            console.log(`L'adresse IP ${ip} est invalide.`);
                        }
                    });
                    req.end();
                } catch (error) {
                    console.log(`L'adresse IP ${ip} est invalide.`);
                }
            }

            const requests = validIPs.map((ip) => coap.request(`coap://${ip}`));
            const responses = await Promise.all(requests);
            const data = responses.map((response) => response.data);
            setData(data);
        };

        fetchData();
    }, []);

    return (
        <div>
            <h1>{title}</h1>
            <ul>
                {data.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
        </div>
    );
};
