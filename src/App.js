import React from "react";

import { PolyLine } from "draw-shape-reactjs";

import { usePersistentCanvas } from "./hooks/usePersistentCanvas";
import "./App.css";

function App() {
  const [locations, setLocations, canvasRef] = usePersistentCanvas();
  function handleCanvasClick(e) {
    setLocations([...locations, { x: e.clientX, y: e.clientY }]);
  }
  return (
    <div className="App">
            <svg >
        <polyline
          points="45 60,36 120, 400 500, 45 60"
          style={{ fill: "none", stroke: "black", "stroke-width": 3 }}
        />
      </svg>
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
