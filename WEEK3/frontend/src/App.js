// Import React library and useState hook for managing state inside the component
import React, { useState } from 'react';

// Import UI components from Ant Design library
import { Button, Input, Card, Space, Typography, message, Divider } from 'antd';

// Import external CSS styles (for grid and node styling)
import './App.css';

// Extract Title and Text components from Typography for easier use
const { Title, Text } = Typography;

// Constant for cell size (50px cell + 5px gap = 55 total spacing)
const CELL_S = 55;

// Main functional component
function App() {

  // --- STATE MANAGEMENT ---

  // nodes: stores all nodes placed on the grid
  // Example: { A: {x:1, y:2, connections: []} }
  const [nodes, setNodes] = useState({});

  // path: stores the shortest path returned from backend (e.g., ['S','A','G'])
  const [path, setPath] = useState([]);

  // inputName: stores user input for naming nodes
  const [inputName, setInputName] = useState("");

  // dragStart: stores the node name where dragging started
  const [dragStart, setDragStart] = useState(null);

  // mousePos: tracks mouse position for drawing "ghost line"
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Function to add a new node to the grid
  const addNode = (x, y) => {

    // Convert input to uppercase and remove spaces
    const name = inputName.trim().toUpperCase();

    // If no name entered → show warning
    if (!name) return message.warning("Please type a Node Name (e.g., S, G, A) first!");

    // Prevent duplicate node names
    if (nodes[name]) return message.error("This node name already exists on the board!");

    // Add new node to state
    setNodes({
      ...nodes, // keep existing nodes
      [name]: { x, y, connections: [] } // add new node
    });

    // Clear input after adding node
    setInputName("");
  };

  // Function triggered when mouse released after dragging
  const handleMouseUp = (targetName) => {

    // Check if drag started and ended on different nodes
    if (dragStart && targetName && dragStart !== targetName) {

      // Get both nodes
      const nodeA = nodes[dragStart];
      const nodeB = nodes[targetName];

      // Calculate Manhattan distance: |x1-x2| + |y1-y2|
      const dist = Math.abs(nodeA.x - nodeB.x) + Math.abs(nodeA.y - nodeB.y);

      // Copy nodes to avoid direct mutation
      const updatedNodes = { ...nodes };

      // Check if connection already exists
      if (!updatedNodes[dragStart].connections.find(c => c.node === targetName)) {

        // Add connection from A → B
        updatedNodes[dragStart].connections.push({
          node: targetName,
          cost: dist
        });

        // Add connection from B → A (bidirectional graph)
        updatedNodes[targetName].connections.push({
          node: dragStart,
          cost: dist
        });

        // Update state
        setNodes(updatedNodes);
      }
    }

    // Reset drag state
    setDragStart(null);
  };

  // Function to call backend API to calculate shortest path
  const calculate = async () => {
    try {

      // Send POST request to backend server
      const res = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },

        // Send start node, goal node, and graph structure
        body: JSON.stringify({
          start_node: "S",
          goal_node: "G",
          nodes
        })
      });

      // Parse JSON response
      const data = await res.json();

      // If a valid path is returned
      if (data.path && data.path.length > 0) {

        // Store path to highlight it in UI
        setPath(data.path);

        // Open new popup window to display results
        const win = window.open("", "_blank", "width=500,height=300");

        // Inject HTML content into new window
        win.document.write(`
          <div style="font-family:sans-serif; text-align:center; padding:40px;">
            <h2 style="color:#1890ff;">Pathfinding Result</h2>

            <!-- Show path -->
            <p style="font-size:22px; font-weight:bold; color:#333;">
              ${data.path.join(" → ")}
            </p>

            <!-- Show cost calculation -->
            <p style="font-size:18px; color:#666;">
              ${data.costs.join(" + ")} = ${data.total_cost} total cost
            </p>

            <hr style="margin-top:20px; border:0; border-top:1px solid #eee;" />

            <!-- Close button -->
            <button onclick="window.close()" style="margin-top:10px; cursor:pointer;">
              Close Window
            </button>
          </div>
        `);

      } else {

        // If no path found
        message.error("No valid path found from S to G. Ensure they are connected!");
      }

    } catch (e) {

      // If backend server is not running
      message.error("Backend Error: Ensure webui-user.bat launched the server on port 8000.");
    }
  };

  // JSX (UI rendering)
  return (

    // Main container with mouse tracking
    <div
      className="container"
      onMouseMove={e => setMousePos({ x: e.clientX, y: e.clientY })}
    >

      {/* Page title */}
      <Title level={2}>A* Manhattan Pathfinder</Title>

      {/* Layout container */}
      <Space align="start" size="large">

        {/* Grid Board */}
        <Card title="Grid Board">

          {/* Input field for node name */}
          <Input
            placeholder="Node Name (Set S and G first)"
            value={inputName}
            onChange={e => setInputName(e.target.value)}
            style={{ marginBottom: 15 }}
          />

          <div className="grid-wrapper">

            {/* SVG for drawing connections */}
            <svg width="550" height="550">

              {/* Draw all connections */}
              {Object.keys(nodes).map(n =>
                nodes[n].connections.map(c => {

                  // Get target node
                  const t = nodes[c.node];

                  return (
                    <g key={n + c.node}>

                      {/* Draw line between nodes */}
                      <line
                        x1={nodes[n].x * CELL_S + 25}
                        y1={nodes[n].y * CELL_S + 25}
                        x2={t.x * CELL_S + 25}
                        y2={t.y * CELL_S + 25}
                        stroke="#1890ff"
                        strokeWidth="2"
                      />

                      {/* Display edge cost */}
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

            {/* Grid cells */}
            <div className="grid-container">

              {/* Generate 10x10 grid */}
              {[...Array(10)].map((_, y) =>
                [...Array(10)].map((_, x) => {

                  // Check if a node exists at this position
                  const name = Object.keys(nodes).find(
                    k => nodes[k].x === x && nodes[k].y === y
                  );

                  // Determine CSS class
                  let cls = "node-cell";

                  if (name === "S") cls += " node-start";
                  else if (name === "G") cls += " node-goal";
                  else if (path.includes(name)) cls += " node-path";
                  else if (name) cls += " node-active";

                  return (
                    <div
                      key={x + "-" + y}
                      className={cls}

                      // Add node if empty cell clicked
                      onClick={() => !name && addNode(x, y)}

                      // Start drag if node exists
                      onMouseDown={() => name && setDragStart(name)}

                      // End drag if node exists
                      onMouseUp={() => name && handleMouseUp(name)}
                    >
                      {/* Display node name */}
                      {name}
                    </div>
                  );
                })
              )}

            </div>
          </div>
        </Card>

        {/* Sidebar tools */}
        <Card title="Tools" style={{ width: 280 }}>

          <Space direction="vertical" style={{ width: '100%' }} size="middle">

            {/* Button to calculate path */}
            <Button type="primary" block size="large" onClick={calculate}>
              Find Path
            </Button>

            {/* Reset everything */}
            <Button block onClick={() => { setNodes({}); setPath([]); }}>
              Reset Board
            </Button>

            <Divider style={{ margin: '12px 0' }} />

            {/* Instructions */}
            <div style={{
              background: '#fafafa',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #f0f0f0'
            }}>

              <Text strong style={{ display: 'block', marginBottom: '8px' }}>
                Instructions:
              </Text>

              <ul style={{
                paddingLeft: '18px',
                margin: 0,
                fontSize: '13px',
                color: '#666'
              }}>
                <li>Type <b>'S'</b> and click a cell for Start.</li>
                <li>Type <b>'G'</b> and click a cell for Goal.</li>
                <li>Add other nodes (A, B, C...) similarly.</li>
                <li><b>Drag</b> between nodes to create a connection.</li>
                <li>Click <b>Find Path</b> to solve.</li>
              </ul>

            </div>

          </Space>
        </Card>

      </Space>
    </div>
  );
}

// Export component so it can be used in index.js
export default App;