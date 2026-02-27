import random
import heapq


class VacuumEnvironment:
    def __init__(self, size=4):
        self.size = size
        self.start = (0, 0)
        self.grid = [["." for _ in range(size)] for _ in range(size)]
        self.dirt_positions = []
        self.unreachable = []

        self.place_obstacles()
        self.place_one_dirt()

    def place_obstacles(self):
        obstacle_count = 3
        count = 0
        while count < obstacle_count:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if (r, c) != self.start and self.grid[r][c] == ".":
                self.grid[r][c] = "#"
                count += 1

    def place_one_dirt(self):
        while True:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if (r, c) != self.start and self.grid[r][c] == ".":
                self.dirt_positions.append((r, c))
                break


def solve_vacuum(env):
    start = env.start
    dirt = env.dirt_positions[0]

    path, cost = a_star(env, start, dirt)

    if path is None:
        env.unreachable.append(dirt)
        return [], 0, env.unreachable

    return path, cost, []


def a_star(env, start, goal):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]

        for dr, dc in moves:
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < env.size and 0 <= nc < env.size:
                if env.grid[nr][nc] == "#":
                    continue

                neighbor = (nr, nc)

                move_cost = movement_cost(current, neighbor)
                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

    return None, float("inf")


def movement_cost(a, b):
    if b[0] < a[0]:   # up
        return 2
    if b[0] > a[0]:   # down
        return 0
    return 1          # left or right


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
