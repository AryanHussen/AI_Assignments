// Import React and useState hook for managing component state
import React, { useState } from 'react';

// Import UI components from Ant Design library
import { Button, Input, Card, Space, Typography, message, Divider } from 'antd';

// Import CSS styling file
import './App.css';

// Extract Title and Text components from Typography
const { Title, Text } = Typography;

// Define constant cell size (50px cell + 5px gap)
const CELL_S = 55;

// Main functional component
function App() {

  // Store all nodes (S, G, A, B...) with their positions and connections
  const [nodes, setNodes] = useState({});

  // Store the final shortest path returned from backend
  const [path, setPath] = useState([]);

  // Store the current node name typed in the input
  const [inputName, setInputName] = useState("");

  // Store the node where drag connection starts
  const [dragStart, setDragStart] = useState(null);

  // Store mouse position for drawing ghost line while dragging
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Function to add a new node to the grid
  const addNode = (x, y) => {

    // Get input name, remove spaces, convert to uppercase
    const name = inputName.trim().toUpperCase();

    // Show warning if input is empty
    if (!name) return message.warning("Please type a Node Name (e.g., S, G, A) first!");

    // Prevent duplicate node names
    if (nodes[name]) return message.error("This node name already exists on the board!");

    // Add new node with position and empty connections list
    setNodes({ 
      ...nodes, 
      [name]: { x, y, connections: [] } 
    });

    // Clear input field after adding
    setInputName("");
  };

  // Handle finishing a drag-to-connect action
  const handleMouseUp = (targetName) => {

    // Make sure drag started and target is different
    if (dragStart && targetName && dragStart !== targetName) {

      // Get both nodes
      const nodeA = nodes[dragStart];
      const nodeB = nodes[targetName];
      
      // Calculate Manhattan distance (|x1-x2| + |y1-y2|)
      const dist = Math.abs(nodeA.x - nodeB.x) + Math.abs(nodeA.y - nodeB.y);
      
      // Copy nodes object to modify safely
      const updatedNodes = { ...nodes };

      // Prevent duplicate connections
      if (!updatedNodes[dragStart].connections.find(c => c.node === targetName)) {

        // Add connection in both directions (undirected graph)
        updatedNodes[dragStart].connections.push({ node: targetName, cost: dist });
        updatedNodes[targetName].connections.push({ node: dragStart, cost: dist });

        // Update state
        setNodes(updatedNodes);
      }
    }

    // Stop dragging
    setDragStart(null);
  };

  // Call backend to calculate shortest path
  const calculate = async () => {
    try {

      // Send POST request to backend server
      const res = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },

        // Send start, goal and graph nodes
        body: JSON.stringify({ start_node: "S", goal_node: "G", nodes })
      });

      // Convert response to JSON
      const data = await res.json();
      
      // If path found
      if (data.path && data.path.length > 0) {

        // Save path to state
        setPath(data.path);
        
        // Open new popup window to show result
        const win = window.open("", "_blank", "width=500,height=300");

        // Write formatted HTML inside popup
        win.document.write(`
          <div style="font-family:sans-serif; text-align:center; padding:40px;">
            <h2 style="color:#1890ff;">Pathfinding Result</h2>
            <p style="font-size:22px; font-weight:bold; color:#333;">${data.path.join(" → ")}</p>
            <p style="font-size:18px; color:#666;">${data.costs.join(" + ")} = ${data.total_cost} total cost</p>
            <hr style="margin-top:20px; border:0; border-top:1px solid #eee;" />
            <button onclick="window.close()" style="margin-top:10px; cursor:pointer;">Close Window</button>
          </div>
        `);

      } else {

        // Show error if no path found
        message.error("No valid path found from S to G. Ensure they are connected!");
      }

    } catch (e) {

      // Show error if backend not running
      message.error("Backend Error: Ensure main.py is running on port 8000.");
    }
  };

  // Return JSX UI
  return (

    // Main container and track mouse movement
    <div className="container" onMouseMove={e => setMousePos({ x: e.clientX, y: e.clientY })}>

      {/* Page title */}
      <Title level={2}>A* Manhattan Pathfinder</Title>
      
      <Space align="start" size="large">

        {/* Grid Board Card */}
        <Card title="Grid Board">

          {/* Input field for node name */}
          <Input 
            placeholder="Node Name (Set S and G first)" 
            value={inputName} 
            onChange={e => setInputName(e.target.value)} 
            style={{ marginBottom: 15 }}
          />
          
          <div className="grid-wrapper">

            {/* SVG layer for drawing lines between nodes */}
            <svg width="550" height="550">

              {/* Loop through nodes and draw connections */}
              {Object.keys(nodes).map(n => nodes[n].connections.map(c => {

                const t = nodes[c.node];

                return (
                  <g key={n + c.node}>

                    {/* Draw connection line */}
                    <line 
                      x1={nodes[n].x * CELL_S + 25} 
                      y1={nodes[n].y * CELL_S + 25} 
                      x2={t.x * CELL_S + 25} 
                      y2={t.y * CELL_S + 25} 
                      stroke="#1890ff" 
                      strokeWidth="2"
                    />

                    {/* Display cost text */}
                    <text 
                      x={(nodes[n].x * CELL_S + t.x * CELL_S + 50) / 2} 
                      y={(nodes[n].y * CELL_S + t.y * CELL_S + 50) / 2} 
                      className="cost-label"
                    >
                      {c.cost}
                    </text>
                  </g>
                );
              }))}

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
