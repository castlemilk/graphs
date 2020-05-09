import React from 'react';

import { usePersistentCanvas } from "./hooks/usePersistentCanvas"
import './App.css';

function App() {
  const [locations, setLocations, canvasRef] = usePersistentCanvas()
  function handleCanvasClick(e) {
    setLocations([...locations, { x: e.clientX, y: e.clientY }])
  }
  return (
    <div className="App">
     <canvas
          ref={canvasRef}
          width={window.innerWidth}
          height={window.innerHeight}
          onClick={handleCanvasClick}
        /> 
    </div>
  );
}

export default App;
