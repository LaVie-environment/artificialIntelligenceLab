#!/usr/bin/env python3

import pygame
import random
import heapq
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 9
CELL_SIZE = 80
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FPS = 5  # Animation speed

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GOLD = (255, 215, 0)
BLUE = (100, 150, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
DARK_GRAY = (50, 50, 50)

DEPOT_POSITION = (4,4)  # Center at (4, 4) for 9x9 grid

class Robot:
    def __init__(self, name, x, y, color):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.gold_collected = False

    def pos(self):
        return (self.x, self.y)

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def pick(self, environment):
        if environment[self.x][self.y] == 'G':
            self.gold_collected = True
            environment[self.x][self.y] = '.'
            return True
        return False

    def drop(self):
        if self.gold_collected:
            self.gold_collected = False
            return True
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Navigate a grid environment to collect gold")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize environment
        self.environment = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.setup_environment()
        
        # Initialize robots
        self.r1 = Robot('R1', DEPOT_POSITION[0], DEPOT_POSITION[1], BLUE)
        self.r2 = Robot('R2', DEPOT_POSITION[0], DEPOT_POSITION[1], RED)
        
        self.gold_collected = 0
        self.total_gold = 5
        self.message = "Press SPACE to start simulation"
        self.running = False
        self.current_path = []

    def setup_environment(self):
        placed_positions = set()
        
        # Place 5 pieces of gold
        gold_count = 0
        while gold_count < 5:
            gx, gy = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if (gx, gy) not in placed_positions and (gx, gy) != DEPOT_POSITION:
                self.environment[gx][gy] = 'G'
                placed_positions.add((gx, gy))
                gold_count += 1
        
        # Place 6 obstacles
        obstacle_count = 0
        while obstacle_count < 10:
            ox, oy = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if (ox, oy) not in placed_positions and (ox, oy) != DEPOT_POSITION:
                self.environment[ox][oy] = '#'
                placed_positions.add((ox, oy))
                obstacle_count += 1

    def manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if self.environment[nx][ny] != '#':
                    neighbors.append((nx, ny))
        return neighbors

    def astar(self, start_x, start_y, goal_x, goal_y):
        start = (start_x, start_y)
        goal = (goal_x, goal_y)
        
        counter = 0
        heap = [(0, counter, start, [start])]
        visited = set()
        g_score = {start: 0}
        
        while heap:
            f, _, current, path = heapq.heappop(heap)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current == goal:
                return path
            
            cx, cy = current
            
            for neighbor in self.get_neighbors(cx, cy):
                if neighbor in visited:
                    continue
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    h = self.manhattan_distance(neighbor[0], neighbor[1], goal_x, goal_y)
                    f_score = tentative_g + h
                    counter += 1
                    new_path = path + [neighbor]
                    heapq.heappush(heap, (f_score, counter, neighbor, new_path))
        
        return None

    def draw_grid(self):
        # Draw cells
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Cell background
                if (x, y) == DEPOT_POSITION:
                    pygame.draw.rect(self.screen, GREEN, rect)
                else:
                    pygame.draw.rect(self.screen, WHITE, rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, BLACK, rect, 2)
                
                # Draw obstacles
                if self.environment[x][y] == '#':
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)
                
                # Draw gold
                elif self.environment[x][y] == 'G':
                    center = (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.circle(self.screen, GOLD, center, CELL_SIZE // 3)
                    pygame.draw.circle(self.screen, BLACK, center, CELL_SIZE // 3, 2)
        
        # Draw current path
        if self.current_path:
            for i in range(len(self.current_path) - 1):
                x1, y1 = self.current_path[i]
                x2, y2 = self.current_path[i + 1]
                start_pos = (y1 * CELL_SIZE + CELL_SIZE // 2, x1 * CELL_SIZE + CELL_SIZE // 2)
                end_pos = (y2 * CELL_SIZE + CELL_SIZE // 2, x2 * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.line(self.screen, (255, 0, 255), start_pos, end_pos, 3)
        
        # Draw robots
        self.draw_robot(self.r1)
        if self.r1.pos() != self.r2.pos():
            self.draw_robot(self.r2)

    def draw_robot(self, robot):
        center = (robot.y * CELL_SIZE + CELL_SIZE // 2, robot.x * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(self.screen, robot.color, center, CELL_SIZE // 4)
        pygame.draw.circle(self.screen, BLACK, center, CELL_SIZE // 4, 2)
        
        # Draw gold indicator if carrying
        if robot.gold_collected:
            pygame.draw.circle(self.screen, GOLD, 
                             (center[0], center[1] - CELL_SIZE // 6), 
                             CELL_SIZE // 8)

    def draw_info(self):
        info_y = WINDOW_SIZE + 10
        
        # Draw message
        text = self.small_font.render(self.message, True, BLACK)
        self.screen.blit(text, (10, info_y))
        
        # Draw gold counter
        gold_text = self.font.render(f"Gold: {self.gold_collected}/{self.total_gold}", True, GOLD)
        self.screen.blit(gold_text, (10, info_y + 30))
        
        # Draw instructions
        if not self.running:
            inst_text = self.small_font.render("SPACE: Start | R: Reset | ESC: Quit", True, BLACK)
            self.screen.blit(inst_text, (WINDOW_SIZE - 350, info_y + 35))

    def simulate_step(self):
        gold_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) 
                          if self.environment[x][y] == 'G']
        
        if not gold_positions:
            self.message = "All gold collected!"
            self.running = False
            return False
        
        # Get next gold
        gx, gy = gold_positions[0]
        
        # Path to gold
        path_to_gold = self.astar(self.r1.x, self.r1.y, gx, gy)
        if path_to_gold is None:
            self.message = f"No path to gold at ({gx}, {gy})"
            return False
        
        # Animate movement to gold
        self.current_path = path_to_gold
        for px, py in path_to_gold[1:]:
            self.r1.move_to(px, py)
            self.message = f"Moving to gold at ({gx}, {gy})"
            self.draw()
            pygame.time.wait(200)
        
        # Pick gold
        self.r1.pick(self.environment)
        self.message = f"Picked up gold at ({gx}, {gy})"
        self.draw()
        pygame.time.wait(500)
        
        # Path to depot
        path_to_depot = self.astar(self.r1.x, self.r1.y, DEPOT_POSITION[0], DEPOT_POSITION[1])
        if path_to_depot is None:
            self.message = "No path back to depot!"
            return False
        
        # Animate movement to depot
        self.current_path = path_to_depot
        for px, py in path_to_depot[1:]:
            self.r1.move_to(px, py)
            self.message = "Returning to depot"
            self.draw()
            pygame.time.wait(200)
        
        # Drop and process
        self.r1.drop()
        self.gold_collected += 1
        self.message = f"Gold processed! ({self.gold_collected}/{self.total_gold})"
        self.current_path = []
        self.draw()
        pygame.time.wait(500)
        
        return True

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_info()
        pygame.display.flip()

    def reset(self):
        self.environment = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.setup_environment()
        self.r1 = Robot('R1', DEPOT_POSITION[0], DEPOT_POSITION[1], BLUE)
        self.r2 = Robot('R2', DEPOT_POSITION[0], DEPOT_POSITION[1], RED)
        self.gold_collected = 0
        self.message = "Environment reset. Press SPACE to start"
        self.running = False
        self.current_path = []

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    if event.key == pygame.K_SPACE and not self.running:
                        self.running = True
                        self.message = "Simulation running..."
                    
                    if event.key == pygame.K_r:
                        self.reset()
            
            if self.running:
                if not self.simulate_step():
                    self.running = False
            
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()