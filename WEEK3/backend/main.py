# Member 1: Backend Engineering - A* Pathfinding Logic
# Language: Python | Framework: FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Tuple, Any

# Step 1: Initialize the FastAPI server instance
# This object 'app' will handle all incoming web requests from the React frontend.
app = FastAPI()

# Step 2: Configure Cross-Origin Resource Sharing (CORS)
# This is mandatory for Software Engineering projects where the Frontend (Port 3000) 
# and Backend (Port 8000) run on different local ports.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your React app to send requests to this script.
    allow_methods=["*"], # Allows all HTTP actions (POST, GET, OPTIONS).
    allow_headers=["*"], # Allows any custom metadata headers in the request.
)

# Step 3: Define the Data Structure (Schema)
# This class ensures the JSON data sent by Member 3 (Integration) is valid.
class PathRequest(BaseModel):
    start_node: str       # The label for the starting point, usually "S".
    goal_node: str        # The label for the target point, usually "G".
    nodes: Dict[str, Any] # A dictionary containing the grid coordinates and connections.

# Step 4: The Heuristic Function (Manhattan Distance)
# Calculation: |x1 - x2| + |y1 - y2|
# This represents the "h" in the A* formula: f(n) = g(n) + h(n).
def get_manhattan(p1, p2):
    # Returns the absolute sum of the differences between X and Y coordinates.
    # We use Manhattan because the grid restricts movement to four directions (Up, Down, Left, Right).
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Step 5: The Primary Pathfinding Endpoint
@app.post("/solve")
async def solve(data: PathRequest):
    # Extract the data sent from the React Frontend.
    start, goal = data.start_node, data.goal_node
    nodes = data.nodes
    
    # Validation: Ensure both 'S' and 'G' are actually placed on the grid.
    if start not in nodes or goal not in nodes:
        return {"path": [], "costs": [], "total_cost": 0}

    # Pre-fetch the goal's (x, y) coordinates for heuristic comparison.
    goal_coords = (nodes[goal]['x'], nodes[goal]['y'])
    
    # --- A* Algorithm Initialization ---
    
    # open_set: A list of nodes discovered but not yet fully explored.
    open_set = {start}
    
    # came_from: Tracks the 'Parent' of each node to reconstruct the path later.
    # Format: {child_node: (parent_node, connection_weight)}
    came_from = {} 
    
    # g_score: The exact cost to reach a node from the start.
    # We initialize all nodes to 'Infinity' because we haven't found a path to them yet.
    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0 # The cost to move from Start to Start is zero.
    
    # f_score: The predicted total cost (Actual Cost + Estimated Distance to Goal).
    f_score = {node: float('inf') for node in nodes}
    # For the start node, f_score is purely the Manhattan distance to the Goal.
    f_score[start] = get_manhattan((nodes[start]['x'], nodes[start]['y']), goal_coords)

    # Begin searching through the grid.
    while open_set:
        # Optimization: Pick the node in our 'open_set' with the lowest predicted f_score.
        # This makes A* much more efficient than Dijkstra’s algorithm.
        current = min(open_set, key=lambda n: f_score[n])
        
        # --- SUCCESS CONDITION ---
        # If the current node is the 'Goal', we have successfully found the shortest path.
        if current == goal:
            path = []  # To store the names of the nodes (e.g., S, A, G).
            costs = [] # To store the weight of each link (e.g., 1, 3, 5).
            temp = current
            # Trace back from Goal to Start using our 'came_from' map.
            while temp in came_from:
                prev, weight = came_from[temp]
                path.append(temp)
                costs.append(weight)
                temp = prev # Move up to the parent node.
            path.append(start) # Finally, add the starting node to the list.
            
            # Return the path and costs reversed so they read correctly (Start to Goal).
            return {
                "path": path[::-1], 
                "costs": costs[::-1], 
                "total_cost": g_score[goal] # The total cost calculated by the algorithm.
            }

        # Exploration: Move the current node from 'to-explore' to 'visited'.
        open_set.remove(current)
        
        # --- EXPLORING NEIGHBORS ---
        # Look at every node connected to our current node.
        for conn in nodes[current].get('connections', []):
            neighbor, weight = conn['node'], conn['cost']
            
            # Calculate the cost to reach this neighbor if we pass through the current node.
            tentative_g = g_score[current] + weight
            
            # If this path to the neighbor is shorter than any path found previously:
            if tentative_g < g_score.get(neighbor, float('inf')):
                # Update our records with this new, better path.
                came_from[neighbor] = (current, weight)
                g_score[neighbor] = tentative_g
                # Recalculate f(n) = g(n) + h(n).
                f_score[neighbor] = tentative_g + get_manhattan(
                    (nodes[neighbor]['x'], nodes[neighbor]['y']), goal_coords
                )
                
                # If we haven't seen this neighbor before, add it to our exploration list.
                if neighbor not in open_set:
                    open_set.add(neighbor)
                    
    # If the loop finishes without reaching the goal, no connection exists.
    return {"path": [], "costs": [], "total_cost": 0}
