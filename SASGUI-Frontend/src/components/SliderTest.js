import React, { useState, useEffect } from 'react';
import Slider from './components/Slider';

const App = () => {
    const [sliders, setSliders] = useState([1, 1, 1, 1, 1, 1]);
    const [graph, setGraph] = useState('');

    const handleSliderChange = (index, value) => {
        const newSliders = [...sliders];
        newSliders[index] = value;
        setSliders(newSliders);
    };

    useEffect(() => {
        // Send slider values to the backend
        fetch('http://127.0.0.1:5000/update_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sliders }),
        })
            .then((response) => response.json())
            .then((data) => {
                setGraph(data.graph);
            });
    }, [sliders]);

    return (
        <div>
            <h1>Real-Time Graph with Sliders</h1>
            {sliders.map((value, index) => (
                <Slider
                    key={index}
                    label={`Slider ${index + 1}`}
                    value={value}
                    onChange={(newValue) => handleSliderChange(index, newValue)}
                />
            ))}
            <div>
                <img src={`data:image/png;base64,${graph}`} alt="Graph" />
            </div>
        </div>
    );
};

export default App;
