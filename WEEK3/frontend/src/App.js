import React, { useState } from 'react';
import { Button, Input, Card, Space, Typography, message, Divider } from 'antd';
import './App.css'; // Import Member 2's visual styles

const { Title, Text } = Typography;
const CELL_S = 55; // Constant for cell size (50px) + gap (5px) for coordinate math

function App() {
  // --- STATE MANAGEMENT ---
  // nodes: Stores all points placed on the grid { 'A': {x: 1, y: 2, connections: []} }
  const [nodes, setNodes] = useState({});
  // path: Stores the array of node names returned by the AI (e.g., ['S', 'A', 'G'])
  const [path, setPath] = useState([]);
  // inputName: Tracks the text typed in the input box for the next node
  const [inputName, setInputName] = useState("");
  // dragStart: Stores the name of the node where a drag-to-connect gesture began
  const [dragStart, setDragStart] = useState(null);
  // mousePos: Tracks the current mouse coordinates for the "ghost" connection line
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Function to add a new node (S, G, or intermediate letters) to the grid
  const addNode = (x, y) => {
    const name = inputName.trim().toUpperCase(); // Normalize input to uppercase
    if (!name) return message.warning("Please type a Node Name (e.g., S, G, A) first!");
    if (nodes[name]) return message.error("This node name already exists on the board!");
    
    // Add new node object to the state
    setNodes({ 
      ...nodes, 
      [name]: { x, y, connections: [] } 
    });
    setInputName(""); // Clear input after adding
  };

  // Logic to handle the end of a drag-to-connect gesture
  const handleMouseUp = (targetName) => {
    if (dragStart && targetName && dragStart !== targetName) {
      const nodeA = nodes[dragStart];
      const nodeB = nodes[targetName];
      
      // Calculate Manhattan distance (|x1-x2| + |y1-y2|) as the edge cost
      const dist = Math.abs(nodeA.x - nodeB.x) + Math.abs(nodeA.y - nodeB.y);
      
      const updatedNodes = { ...nodes };
      // Prevent duplicate connections between the same two nodes
      if (!updatedNodes[dragStart].connections.find(c => c.node === targetName)) {
        // Add bidirectional connection (A -> B and B -> A)
        updatedNodes[dragStart].connections.push({ node: targetName, cost: dist });
        updatedNodes[targetName].connections.push({ node: dragStart, cost: dist });
        setNodes(updatedNodes);
      }
    }
    setDragStart(null); // Reset drag state
  };

  // Function to call the FastAPI Backend (Member 1) to solve the path
  const calculate = async () => {
    try {
      const res = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_node: "S", goal_node: "G", nodes })
      });
      const data = await res.json();
      
      if (data.path && data.path.length > 0) {
        setPath(data.path); // Highlight the path on the grid
        
        // Open the solution window with the mathematical breakdown
        const win = window.open("", "_blank", "width=500,height=300");
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
        message.error("No valid path found from S to G. Ensure they are connected!"); 
      }
    } catch (e) { 
      message.error("Backend Error: Ensure webui-user.bat launched the server on port 8000."); 
    }
  };

  return (
    <div className="container" onMouseMove={e => setMousePos({ x: e.clientX, y: e.clientY })}>
      <Title level={2}>A* Manhattan Pathfinder</Title>
      
      <Space align="start" size="large">
        <Card title="Grid Board">
          <Input 
            placeholder="Node Name (Set S and G first)" 
            value={inputName} 
            onChange={e => setInputName(e.target.value)} 
            style={{ marginBottom: 15 }}
          />
          
          <div className="grid-wrapper">
            {/* SVG Layer: Draws the connection lines and edge costs */}
            <svg width="550" height="550">
              {Object.keys(nodes).map(n => nodes[n].connections.map(c => {
                const t = nodes[c.node];
                return (
                  <g key={n + c.node}>
                    <line 
                      x1={nodes[n].x * CELL_S + 25} 
                      y1={nodes[n].y * CELL_S + 25} 
                      x2={t.x * CELL_S + 25} 
                      y2={t.y * CELL_S + 25} 
                      stroke="#1890ff" 
                      strokeWidth="2"
                    />
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
              
              {/* Ghost Line: Follows the mouse during a drag connection gesture */}
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

            {/* Grid Container: Renders the 10x10 board cells */}
            <div className="grid-container">
              {[...Array(10)].map((_, y) => [...Array(10)].map((_, x) => {
                const name = Object.keys(nodes).find(k => nodes[k].x === x && nodes[k].y === y);
                
                // Determine CSS class based on node type for Member 2's styling
                let cls = "node-cell";
                if (name === "S") cls += " node-start";
                else if (name === "G") cls += " node-goal";
                else if (path.includes(name)) cls += " node-path";
                else if (name) cls += " node-active";

                return (
                  <div 
                    key={x + "-" + y} 
                    className={cls} 
                    onClick={() => !name && addNode(x, y)} 
                    onMouseDown={() => name && setDragStart(name)} 
                    onMouseUp={() => name && handleMouseUp(name)}
                  >
                    {name}
                  </div>
                );
              }))}
            </div>
          </div>
        </Card>

        {/* Sidebar Tools Panel */}
        <Card title="Tools" style={{ width: 280 }}>
          <Space direction="vertical" style={{ width: '100%' }} size="middle">
            <Button type="primary" block size="large" onClick={calculate}>
              Find Path
            </Button>
            <Button block onClick={() => { setNodes({}); setPath([]); }}>
              Reset Board
            </Button>
            
            <Divider style={{ margin: '12px 0' }} />
            
            <div style={{ background: '#fafafa', padding: '12px', borderRadius: '8px', border: '1px solid #f0f0f0' }}>
              <Text strong style={{ display: 'block', marginBottom: '8px' }}>Instructions:</Text>
              <ul style={{ paddingLeft: '18px', margin: 0, fontSize: '13px', color: '#666' }}>
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

export default App;