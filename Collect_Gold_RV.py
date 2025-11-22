#!/usr/bin/env python3

import random
import heapq

GRID_SIZE = 9
DEPOT_POSITION = (4,4)  # Center at (4, 4) for 9x9 grid


'''
This Robot class creates a blueplrint for robot objects that can move around the grid and interact with gold.
'''
class Robot:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.gold_collected = False # Tracks whether the robot is carrying gold

    def pos(self):
        return (self.x, self.y)

    def move_to(self, x, y):
        """Move the robot to a specific position."""
        self.x = x
        self.y = y

    def pick(self):
        """Pick up gold if on the same position."""
        if environment[self.x][self.y] == 'G':
            self.gold_collected = True
            environment[self.x][self.y] = '.'
            print(f"{self.name} picked up gold at ({self.x}, {self.y})")

    def drop(self):
        """Drop gold at current position if holding any."""
        if self.gold_collected:
            print(f"{self.name} dropped gold at ({self.x}, {self.y})")
            self.gold_collected = False

class CollectingRobot(Robot):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

class DepotRobot(Robot):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

    def process(self):
        """Process gold at depot position."""
        if self.pos() == DEPOT_POSITION:
            print(f"{self.name} processed gold at depot ({self.x}, {self.y})")

# Initialize environment
environment = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place gold and obstacles ensuring no overlap
placed_positions = set()

# Place 5 pieces of gold
gold_count = 0
while gold_count < 5:
    gx, gy = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    if (gx, gy) not in placed_positions and (gx, gy) != DEPOT_POSITION:
        environment[gx][gy] = 'G'
        placed_positions.add((gx, gy))
        gold_count += 1

# Place 10 obstacles
obstacle_count = 0
while obstacle_count < 10:
    ox, oy = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    if (ox, oy) not in placed_positions and (ox, oy) != DEPOT_POSITION:
        environment[ox][oy] = '#'
        placed_positions.add((ox, oy))
        obstacle_count += 1

# Initialize robots at center
r1 = CollectingRobot('r1', DEPOT_POSITION[0], DEPOT_POSITION[1])
r2 = DepotRobot('r2', DEPOT_POSITION[0], DEPOT_POSITION[1])

def manhattan_distance(x1, y1, x2, y2):
    """Heuristic function for A*."""
    return abs(x1 - x2) + abs(y1 - y2)

def get_neighbors(x, y):
    """Get valid neighboring cells (4-directional movement)."""
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            if environment[nx][ny] != '#':  # Not an obstacle
                neighbors.append((nx, ny))
    return neighbors

def astar(start_x, start_y, goal_x, goal_y):
    """A* pathfinding algorithm."""
    start = (start_x, start_y)
    goal = (goal_x, goal_y)
    
    # Priority queue: (f_score, counter, position, path)
    counter = 0
    heap = [(0, counter, start, [start])]
    visited = set()
    
    # g_score: cost from start to current node
    g_score = {start: 0}
    
    while heap:
        f, _, current, path = heapq.heappop(heap)
        
        if current in visited:
            continue
            
        visited.add(current)
        
        if current == goal:
            return path
        
        cx, cy = current
        
        for neighbor in get_neighbors(cx, cy):
            if neighbor in visited:
                continue
            
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                h = manhattan_distance(neighbor[0], neighbor[1], goal_x, goal_y)
                f_score = tentative_g + h
                counter += 1
                new_path = path + [neighbor]
                heapq.heappush(heap, (f_score, counter, neighbor, new_path))
    
    return None  # No path found

def print_environment():
    """Display the environment grid with robot positions."""
    grid_copy = [row[:] for row in environment] # list comprehension
    
    # Mark robot positions
    if r1.pos() == r2.pos():
        grid_copy[r1.x][r1.y] = 'R'  # Both at same position
    else:
        if environment[r1.x][r1.y] != 'G':
            grid_copy[r1.x][r1.y] = '1'
        if environment[r2.x][r2.y] != 'G':
            grid_copy[r2.x][r2.y] = '2'
    
        # Print top border
    print('┌' + '───┬' * (GRID_SIZE - 1) + '───┐')
    
    # Print each row with borders
    for i, row in enumerate(grid_copy):
        print('│', end='')
        for cell in row:
            print(f' {cell} │', end='')
        print()
        
        # Print separator between rows (but not after last row)
        if i < GRID_SIZE - 1:
            print('├' + '───┼' * (GRID_SIZE - 1) + '───┤')
    
    # Print bottom border
    print('└' + '───┴' * (GRID_SIZE - 1) + '───┘')
    print()

     # for row in grid_copy:
         # print(' '.join(row))
     # print()

def simulate():
    """Simulate robot gold collection using A* pathfinding."""
    gold_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) 
                      if environment[x][y] == 'G']
    
    print(f"Found {len(gold_positions)} pieces of gold to collect\n")
    
    for idx, (gx, gy) in enumerate(gold_positions, 1):
        print(f"=== Collecting gold piece {idx}/{len(gold_positions)} at ({gx}, {gy}) ===")
        
        # Find path from current position to gold
        path_to_gold = astar(r1.x, r1.y, gx, gy)
        
        if path_to_gold is None:
            print(f"No path found to gold at ({gx}, {gy})!")
            continue
        
        # Move along the path to gold
        for step, (px, py) in enumerate(path_to_gold[1:], 1):
            r1.move_to(px, py)
            print(f"{r1.name} moved to ({r1.x}, {r1.y}) [step {step}/{len(path_to_gold)-1}]")
        
        r1.pick()
        
        # Find path back to depot
        path_to_depot = astar(r1.x, r1.y, DEPOT_POSITION[0], DEPOT_POSITION[1])
        
        if path_to_depot is None:
            print(f"No path found back to depot!")
            continue
        
        # Move along the path to depot
        for step, (px, py) in enumerate(path_to_depot[1:], 1):
            r1.move_to(px, py)
            print(f"{r1.name} moved to ({r1.x}, {r1.y}) [step {step}/{len(path_to_depot)-1}]")
        
        r1.drop()
        r2.process()
        print()

print("Initial Environment:")
print("Legend: . = empty, G = gold, # = obstacle, R = robots (at depot)")
print_environment()

simulate()

print("Final Environment:")
print_environment()