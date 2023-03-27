import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
    const [data, setData] = useState([]);

    // Ajouter le titre du projet
    const title = "Mon projet";

    useEffect(() => {
        const fetchData = async () => {
            const validIPs = [];

            // Vérifier les adresses IP valides
            for (let i = 10; i <= 254; i++) {
                const ip = `10.0.0.${i}`;
                try {
                    await axios.get(`http://${ip}`);
                    validIPs.push(ip);
                } catch (error) {
                    console.log(`L'adresse IP ${ip} est invalide.`);
                }
            }

            // Récupérer les données des adresses IP valides
            const requests = validIPs.map((ip) => axios.get(`http://${ip}`));
            const responses = await Promise.all(requests);
            const data = responses.map((response) => response.data);
            setData(data);
        };

        fetchData();
    }, []);

    return (
        <div>
            {/* Afficher le titre du projet */}
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
