// Import React and the useState hook (for managing state inside the component)
import React, { useState } from 'react';

// Import UI components from Ant Design library
import { Button, Input, Card, Space, Typography, message, Divider } from 'antd';

// Import CSS styling file
import './App.css';

// Extract Title and Text components from Typography
const { Title, Text } = Typography;

// Size of each grid cell (50px cell + 5px gap)
const CELL_S = 55;

function App() {

  // nodes object:
  // {
  //   A: { x: 1, y: 2, connections: [{ node: 'B', cost: 3 }] }
  // }
  const [nodes, setNodes] = useState({}); // stores all nodes on board

  const [path, setPath] = useState([]); // stores shortest path result (like ["S","A","G"])

  const [inputName, setInputName] = useState(""); // stores input text for node name

  const [dragStart, setDragStart] = useState(null); 
  // stores which node we started dragging from

  const [mousePos, setMousePos] = useState({ x: 0, y: 0 }); 
  // stores mouse position (used for drawing ghost line)

  // =========================
  // Add new node to grid
  // =========================
  const addNode = (x, y) => {

    const name = inputName.trim().toUpperCase(); 
    // remove spaces and convert to uppercase

    if (!name) 
      return message.warning("Please type a Node Name (e.g., S, G, A) first!");

    if (nodes[name]) 
      return message.error("This node name already exists on the board!");

    // Add new node into nodes object
    setNodes({ 
      ...nodes, // keep old nodes
      [name]: { x, y, connections: [] } // add new one
    });

    setInputName(""); // clear input box
  };

  // =========================
  // When user finishes dragging
  // =========================
  const handleMouseUp = (targetName) => {

    // Only connect if:
    // - we started dragging
    // - target exists
    // - not connecting to itself
    if (dragStart && targetName && dragStart !== targetName) {

      const nodeA = nodes[dragStart];
      const nodeB = nodes[targetName];

      // Manhattan distance formula:
      // |x1 - x2| + |y1 - y2|
      const dist = Math.abs(nodeA.x - nodeB.x) + 
                   Math.abs(nodeA.y - nodeB.y);

      const updatedNodes = { ...nodes };

      // prevent duplicate connection
      if (!updatedNodes[dragStart].connections.find(c => c.node === targetName)) {

        // add connection both ways (undirected graph)
        updatedNodes[dragStart].connections.push({ node: targetName, cost: dist });
        updatedNodes[targetName].connections.push({ node: dragStart, cost: dist });

        setNodes(updatedNodes); // update state
      }
    }

    setDragStart(null); // reset drag
  };

  // =========================
  // Call backend to calculate A* path
  // =========================
  const calculate = async () => {

    try {
      const res = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },

        // Send nodes + start + goal to backend
        body: JSON.stringify({ 
          start_node: "S", 
          goal_node: "G", 
          nodes 
        })
      });

      const data = await res.json();

      if (data.path && data.path.length > 0) {

        setPath(data.path); // save path in state

        // open small popup window to show result
        const win = window.open("", "_blank", "width=500,height=300");

        win.document.write(`
          <div style="font-family:sans-serif; text-align:center; padding:40px;">
            <h2 style="color:#1890ff;">Pathfinding Result</h2>

            <!-- show path -->
            <p style="font-size:22px; font-weight:bold; color:#333;">
              ${data.path.join(" → ")}
            </p>

            <!-- show cost math -->
            <p style="font-size:18px; color:#666;">
              ${data.costs.join(" + ")} = ${data.total_cost} total cost
            </p>

            <hr style="margin-top:20px; border:0; border-top:1px solid #eee;" />

            <button onclick="window.close()" 
              style="margin-top:10px; cursor:pointer;">
              Close Window
            </button>
          </div>
        `);

      } else {
        message.error("No valid path found from S to G.");
      }

    } catch (e) {
      message.error("Backend Error: Ensure main.py is running.");
    }
  };

  // =========================
  // UI Rendering
  // =========================
  return (

    <div 
      className="container" 
      onMouseMove={e => 
        setMousePos({ x: e.clientX, y: e.clientY })
      }
    >

      <Title level={2}>A* Manhattan Pathfinder</Title>

      <Space align="start" size="large">

        {/* Left Card (Grid) */}
        <Card title="Grid Board">

          <Input 
            placeholder="Node Name (Set S and G first)" 
            value={inputName}
            onChange={e => setInputName(e.target.value)}
            style={{ marginBottom: 15 }}
          />

          <div className="grid-wrapper">

            {/* SVG used for drawing lines between nodes */}
            <svg width="550" height="550">

              {/* Draw all connections */}
              {Object.keys(nodes).map(n =>
                nodes[n].connections.map(c => {

                  const t = nodes[c.node];

                  return (
                    <g key={n + c.node}>

                      {/* connection line */}
                      <line 
                        x1={nodes[n].x * CELL_S + 25}
                        y1={nodes[n].y * CELL_S + 25}
                        x2={t.x * CELL_S + 25}
                        y2={t.y * CELL_S + 25}
                        stroke="#1890ff"
                        strokeWidth="2"
                      />

                      {/* cost label */}
                      <text
                        x={(nodes[n].x * CELL_S + t.x * CELL_S + 50) / 2}
                        y={(nodes[n].y * CELL_S + t.y * CELL_S + 50) / 2}
                        className="cost-label"
                      >
                        {c.cost}
                      </text>
                    </g>
                  );
                })
              )}

              {/* Ghost line while dragging */}
              {dragStart && (
                <line 
                  x1={nodes[dragStart].x * CELL_S + 25}
                  y1={nodes[dragStart].y * CELL_S + 25}
                  x2={mousePos.x - 70}
                  y2={mousePos.y - 250}
                  stroke="#ccc"
                  strokeDasharray="5"
                />
              )}
            </svg>

            {/* Grid cells (10x10) */}
            <div className="grid-container">
              {[...Array(10)].map((_, y) =>
                [...Array(10)].map((_, x) => {

                  // check if a node exists in this cell
                  const name = Object.keys(nodes)
                    .find(k => nodes[k].x === x && nodes[k].y === y);

                  let cls = "node-cell";

                  if (name === "S") cls += " node-start";
                  else if (name === "G") cls += " node-goal";
                  else if (path.includes(name)) cls += " node-path";
                  else if (name) cls += " node-active";

                  return (
                    <div
                      key={x + "-" + y}
                      className={cls}

                      // Add node if empty
                      onClick={() => !name && addNode(x, y)}

                      // Start drag if node exists
                      onMouseDown={() => name && setDragStart(name)}

                      // End drag
                      onMouseUp={() => name && handleMouseUp(name)}
                    >
                      {name}
                    </div>
                  );
                })
              )}
            </div>

          </div>
        </Card>

        {/* Right Card (Tools) */}
        <Card title="Tools" style={{ width: 280 }}>
          <Space direction="vertical" style={{ width: '100%' }} size="middle">

            <Button type="primary" block size="large" onClick={calculate}>
              Find Path
            </Button>

            <Button block onClick={() => { 
              setNodes({}); 
              setPath([]); 
            }}>
              Reset Board
            </Button>

            <Divider style={{ margin: '12px 0' }} />

            <div>
              <Text strong>Instructions:</Text>
              <ul>
                <li>Type 'S' for Start</li>
                <li>Type 'G' for Goal</li>
                <li>Add nodes A, B, C...</li>
                <li>Drag to connect nodes</li>
                <li>Click Find Path</li>
              </ul>
            </div>

          </Space>
        </Card>

      </Space>
    </div>
  );
}

export default App; // export component so React can use it
