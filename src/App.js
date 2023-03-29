import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
    const [data, setData] = useState([]);

    const title = "Retrieve the data on unknown IP address and print it with React";

    useEffect(() => {
        const fetchData = async () => {
            const validIPs = [];

            for (let i = 5; i <= 254; i++) {
                const ip = `10.0.0.${i}`;
                try {
                    await axios.get(`http://${ip}`);
                    validIPs.push(ip);
                } catch (error) {
                    console.log(`Invalip IP address ${ip}.`);
                }
            }

            const requests = validIPs.map((ip) => axios.get(`http://${ip}`));
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

export default App;
