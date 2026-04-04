import random  # For generating random positions for dirt and obstacles
import heapq   # For the priority queue used in the A* algorithm


# Define the class that represents the vacuum's world — the grid, obstacles, and dirt
class VacuumEnvironment:
    # Constructor method — called automatically when VacuumEnvironment(size=4) is used
    def __init__(self, size=4):
        self.size = size  # Define the grid dimensions (default 4x4)
        self.start = (0, 0)  # Starting position of the robot — always top-left corner
        self.grid = [["." for _ in range(size)] for _ in range(size)]# Initialize empty grid — 2D list filled with "." meaning clean/passable cells
        self.grid[0][0] = "V"  # Mark the starting cell with "V" to indicate the robot's initial position
        self.dirt_positions = []  # List to store where dirt is placed — will hold (row, col) tuples
        self.unreachable = []     # List for dirt that cannot be reached (blocked by obstacles) — used for reporting

        self.place_obstacles()  # Call method to put walls in the environment — randomly adds "#" cells
        self.place_one_dirt()   # Call method to put one piece of dirt in the environment — randomly adds one dirty cell

    # Method that randomly places a fixed number of obstacles ("#") on the grid
    def place_obstacles(self):
        obstacle_count = 3  # We want exactly 3 obstacles placed on the grid
        count = 0           # Counter to track how many obstacles have been placed so far
        # Keep looping until exactly obstacle_count obstacles have been successfully placed
        while count < obstacle_count:
            r = random.randint(0, self.size - 1)  # Random row index within grid bounds (0 to size-1)
            c = random.randint(0, self.size - 1)  # Random column index within grid bounds (0 to size-1)
            # Ensure obstacle isn't on start point and doesn't overlap existing obstacles
            if (r, c) != self.start and self.grid[r][c] == ".":
                self.grid[r][c] = "#"  # Mark the cell as an obstacle — "#" means impassable wall
                count += 1             # Increment counter since a valid obstacle was successfully placed

    # Method that randomly places exactly one piece of dirt on a free cell
    def place_one_dirt(self):
        # Keep looping until a valid dirt position is found — guarantees dirt lands on a free cell
        while True:
            r = random.randint(0, self.size - 1)  # Random row within grid bounds
            c = random.randint(0, self.size - 1)  # Random column within grid bounds
            # Ensure dirt isn't on start point or on an obstacle — must land on a clean passable cell
            if (r, c) != self.start and self.grid[r][c] == ".":
                self.grid[r][c] = "D"  # Mark the cell as dirty — "D" means this cell has dirt that needs to be cleaned
                self.dirt_positions.append((r, c))  # Add dirt to list as a (row, col) tuple
                break                                # Exit the loop immediately — only one dirt needed


# Top-level function that coordinates solving the vacuum problem using A*
def solve_vacuum(env):
    start = env.start              # Get robot starting point — always (0, 0)
    dirt = env.dirt_positions[0]  # Get the target dirt location — the single (row, col) tuple we need to reach

    # Run A* to find path and total cost — returns the optimal path list and its movement cost
    path, cost = a_star(env, start, dirt)

    if path is None:  # If A* returns None, no valid path exists — all routes are blocked by obstacles
        env.unreachable.append(dirt)  # Track the unreachable target — stored for reporting purposes
        return [], 0, env.unreachable  # Return empty path, zero cost, and the list of unreachable dirt

    return path, cost, []  # Return the calculated path and cost — empty list means all dirt was reachable


# Core A* pathfinding algorithm — finds the lowest-cost path from start to goal on the grid
def a_star(env, start, goal):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible moves: Up, Down, Left, Right — as (row_delta, col_delta) pairs

    open_set = []  # Priority queue for nodes to explore — heapq automatically keeps the lowest f_score at the front
    # Push (priority, current_node) into the heap; priority 0 since we start here with no cost yet
    heapq.heappush(open_set, (0, start))

    came_from = {}  # Dictionary to store the best "parent" of each node (for path reconstruction) — maps node -> node it came from
    g_score = {start: 0}  # Dictionary storing the cheapest cost found so far to reach a node — start costs 0 to reach itself

    # Main A* loop — continues until all reachable nodes have been explored or goal is found
    while open_set:
        # Pop the node with the lowest f_score (priority) — this is the most promising node to explore next
        _, current = heapq.heappop(open_set)

        if current == goal:  # Check if we reached the dirt — goal test happens when a node is popped, not pushed
            path = []        # Initialize an empty list to build the path by tracing backwards
            while current in came_from:  # Trace back from goal to start using parents — stops when we reach the start node (which has no parent)
                path.append(current)     # Add this node to the path as we walk backwards
                current = came_from[current]  # Move to the parent of the current node
            path.append(start)  # Add the starting node to complete the path — start has no entry in came_from so we add it manually
            path.reverse()      # Reverse to get the path from Start -> Goal — tracing was backward so we flip it
            return path, g_score[goal]  # Return path and the final cost — g_score[goal] is the total movement cost

        for dr, dc in moves:  # Check all 4 neighbor directions — iterate over each (row_delta, col_delta) pair
            nr, nc = current[0] + dr, current[1] + dc  # Calculate neighbor coordinates by applying the move delta to current position

            # Boundary check: stay within grid limits — ensures we don't access cells outside the grid array
            if 0 <= nr < env.size and 0 <= nc < env.size:
                if env.grid[nr][nc] == "#":  # Check for obstacles — "#" means this cell is a wall and cannot be entered
                    continue  # Skip this move if it's a wall — jump to the next direction

                neighbor = (nr, nc)  # Package the valid neighbor coordinates as a tuple for use as a dictionary key

                # Calculate cost to move from current node to this neighbor — depends on the direction of movement
                move_cost = movement_cost(current, neighbor)
                tentative_g = g_score[current] + move_cost  # Actual cost from start to neighbor via current node

                # If this path to neighbor is better than any previous one, record it
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current       # Record where we came from — needed to reconstruct the path later
                    g_score[neighbor] = tentative_g     # Update best known cost to this neighbor — overwrite any worse previous cost
                    # f_score = actual_cost (g) + estimated_cost_to_goal (h) — combines known cost with heuristic estimate
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))  # Add to queue for exploration — priority is f_score so best nodes are processed first

    return None, float("inf")  # If queue empties without reaching goal, return Failure — None path and infinite cost signals no solution


# Function that returns the movement cost of stepping from cell a to cell b
def movement_cost(a, b):
    if b[0] < a[0]:   # Checking if the move is "Up" (row index decreases — smaller row = higher on screen)
        return 2      # Moving Up is expensive (cost 2) — penalizes upward movement in the cost model
    if b[0] > a[0]:   # Checking if the move is "Down" (row index increases — larger row = lower on screen)
        return 0      # Moving Down is "free" (cost 0) — rewards downward movement, A* will prefer it
    return 1          # Moving Left or Right costs 1 — horizontal movement has a neutral intermediate cost


# Heuristic function used by A* to estimate the remaining cost from cell a to cell b
def heuristic(a, b):
    # Manhattan distance: sum of absolute differences of coordinates
    # This estimates the minimum moves left to reach the goal
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # |row_a - row_b| + |col_a - col_b| — counts minimum steps ignoring obstacles and costs