import heapq  # Import priority queue to help the AI pick the "best" next step
import random # Import random to make the board different every time you run it

class VacuumEnvironment:
    def __init__(self, size=4, obstacle_prob=0.2):
        self.size = size # Set the grid size (e.g., 4 means a 4x4 board)
        
        # Create a 2D grid filled with '.' to show empty squares
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.obstacles = set() # Create a list to remember where obstacles are placed
        
        # Loop through rows and columns to place random obstacles
        for r in range(size):
            for c in range(size):
                # If a random number is small, put an obstacle here
                if random.random() < obstacle_prob:
                    self.grid[r][c] = '#' # '#' means the vacuum cannot pass here
                    self.obstacles.add((r, c)) # Add to the blocked list

        # Place the Vacuum and the Dirt on empty squares
        self.start = self.get_random_free_pos() # Find a start point for V
        self.goal = self.get_random_free_pos()  # Find a goal point for D
        
        # Put the V and D letters on the grid
        self.grid[self.start[0]][self.start[1]] = 'V'
        self.grid[self.goal[0]][self.goal[1]] = 'D'

    def get_random_free_pos(self):
        # Keep looking until we find a square marked with '.' (not an obstacle)
        while True:
            r, c = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.grid[r][c] == '.':
                return (r, c)

def manhattan_distance(pos, goal):
    # This is the 'Heuristic' that tells the AI how far the dirt is
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def solve_vacuum(env):
    # Priority Queue stores: (distance_to_dirt, current_pos, path_history, total_cost)
    start_node = (manhattan_distance(env.start, env.goal), env.start, [env.start], 0)
    frontier = [start_node] # The list of squares the AI is thinking about visiting
    visited = set() # A list of squares the AI already visited (to avoid loops)

    # Set the movement costs based on your assignment rules
    directions = {
        'UP': (-1, 0, 2),    # Moving UP costs 2
        'DOWN': (1, 0, 0),   # Moving DOWN costs 0
        'LEFT': (0, -1, 1),  # Moving LEFT costs 1
        'RIGHT': (0, 1, 1)   # Moving RIGHT costs 1
    }

    while frontier:
        # Pick the square that is "Best" (closest to the dirt)
        _, current, path, cost = heapq.heappop(frontier)

        # If the current square is the dirt (D), we win!
        if current == env.goal:
            return path, cost # Return the successful steps and the total cost

        # If we already checked this square, move to the next one
        if current in visited:
            continue
        visited.add(current) # Mark this square as "finished"

        # Check all 4 directions around the current square
        for move, (dr, dc, move_cost) in directions.items():
            r, c = current[0] + dr, current[1] + dc
            
            # Boundary check: Is the vacuum still inside the 4x4 board?
            # Obstacle check: Is this square NOT an obstacle (#)?
            if 0 <= r < env.size and 0 <= c < env.size and (r, c) not in env.obstacles:
                new_path = path + [(r, c)] # Add this move to the path
                new_cost = cost + move_cost # Add the cost (0, 1, or 2)
                priority = manhattan_distance((r, c), env.goal) # Guess distance
                heapq.heappush(frontier, (priority, (r, c), new_path, new_cost))

    # If the AI tries everything and can't reach the dirt, return nothing
    return None, 0