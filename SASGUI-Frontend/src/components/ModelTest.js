import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Chart } from 'react-chartjs-2';
import { Canvas } from '@react-three/fiber';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';

const App = () => {
  const [graphData, setGraphData] = useState(null);
  const [model, setModel] = useState(null);

  useEffect(() => {
    // Fetch graph image
    axios.get(`${backend_link}/graph`, { responseType: 'blob' })
      .then(response => {
        const url = URL.createObjectURL(response.data);
        setGraphData(url);
      });

    // Fetch 3D model
    axios.get(`${backend_link}/3d-model`, { responseType: 'blob' })
      .then(response => {
        const url = URL.createObjectURL(response.data);
        setModel(url);
      });
  }, []);

  return (
    <div>
      <h1>Graph and 3D Model</h1>
      {graphData && <img src={graphData} alt="Graph" />}
      {model && (
        <Canvas>
          <ambientLight />
          <pointLight position={[10, 10, 10]} />
          <Model url={model} />
        </Canvas>
      )}
    </div>
  );
};

const Model = ({ url }) => {
  const [obj, setObj] = useState(null);

  useEffect(() => {
    new OBJLoader().load(url, setObj);
  }, [url]);

  return obj ? <primitive object={obj} /> : null;
};

export default App;
