import random  # For generating random positions for dirt and obstacles
import heapq   # For the priority queue used in the A* algorithm


class VacuumEnvironment:
    def __init__(self, size=4):
        self.size = size  # Define the grid dimensions (default 4x4)
        self.start = (0, 0)  # Starting position of the robot
        self.grid = [["." for _ in range(size)] for _ in range(size)]  # Initialize empty grid
        self.dirt_positions = []  # List to store where dirt is placed
        self.unreachable = []     # List for dirt that cannot be reached (blocked by obstacles)

        self.place_obstacles()  # Call method to put walls in the environment
        self.place_one_dirt()   # Call method to put one piece of dirt in the environment

    def place_obstacles(self):
        obstacle_count = 3  # We want exactly 3 obstacles
        count = 0
        while count < obstacle_count:
            r = random.randint(0, self.size - 1)  # Random row index
            c = random.randint(0, self.size - 1)  # Random column index
            # Ensure obstacle isn't on start point and doesn't overlap existing obstacles
            if (r, c) != self.start and self.grid[r][c] == ".":
                self.grid[r][c] = "#"  # Mark the cell as an obstacle
                count += 1

    def place_one_dirt(self):
        while True:
            r = random.randint(0, self.size - 1)  # Random row
            c = random.randint(0, self.size - 1)  # Random column
            # Ensure dirt isn't on start point or on an obstacle
            if (r, c) != self.start and self.grid[r][c] == ".":
                self.dirt_positions.append((r, c))  # Add dirt to list
                break


def solve_vacuum(env):
    start = env.start  # Get robot starting point
    dirt = env.dirt_positions[0]  # Get the target dirt location

    # Run A* to find path and total cost
    path, cost = a_star(env, start, dirt)

    if path is None:  # If A* returns None, no valid path exists
        env.unreachable.append(dirt)  # Track the unreachable target
        return [], 0, env.unreachable  # Return empty results

    return path, cost, []  # Return the calculated path and cost


def a_star(env, start, goal):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible moves: Up, Down, Left, Right

    open_set = []  # Priority queue for nodes to explore
    # Push (priority, current_node) into the heap; priority 0 since we start here
    heapq.heappush(open_set, (0, start))

    came_from = {}  # Dictionary to store the best "parent" of each node (for path reconstruction)
    g_score = {start: 0}  # Dictionary storing the cheapest cost found so far to reach a node

    while open_set:
        # Pop the node with the lowest f_score (priority)
        _, current = heapq.heappop(open_set)

        if current == goal:  # Check if we reached the dirt
            path = []
            while current in came_from:  # Trace back from goal to start using parents
                path.append(current)
                current = came_from[current]
            path.append(start)  # Add the starting node to complete the path
            path.reverse()  # Reverse to get the path from Start -> Goal
            return path, g_score[goal]  # Return path and the final cost

        for dr, dc in moves:  # Check all 4 neighbor directions
            nr, nc = current[0] + dr, current[1] + dc  # Calculate neighbor coordinates

            # Boundary check: stay within grid limits
            if 0 <= nr < env.size and 0 <= nc < env.size:
                if env.grid[nr][nc] == "#":  # Check for obstacles
                    continue  # Skip this move if it's a wall

                neighbor = (nr, nc)

                # Calculate cost to move from current node to this neighbor
                move_cost = movement_cost(current, neighbor)
                tentative_g = g_score[current] + move_cost  # Actual cost from start to neighbor

                # If this path to neighbor is better than any previous one, record it
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current  # Record where we came from
                    g_score[neighbor] = tentative_g  # Update best known cost to this neighbor
                    # f_score = actual_cost (g) + estimated_cost_to_goal (h)
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))  # Add to queue for exploration

    return None, float("inf")  # If queue empties without reaching goal, return Failure


def movement_cost(a, b):
    if b[0] < a[0]:   # Checking if the move is "Up" (row index decreases)
        return 2      # Moving Up is expensive (cost 2)
    if b[0] > a[0]:   # Checking if the move is "Down" (row index increases)
        return 0      # Moving Down is "free" (cost 0)
    return 1          # Moving Left or Right costs 1


def heuristic(a, b):
    # Manhattan distance: sum of absolute differences of coordinates
    # This estimates the minimum moves left to reach the goal
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
