#!/usr/bin/env python3

import random

GRID_SIZE = 7
R2_POSITION = (GRID_SIZE // 2, GRID_SIZE // 2)

class Robot:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.garbage_collected = False

    def pos(self):
        return (self.x, self.y)

    def move_towards(self, target_x, target_y):
        """Move the robot one step closer to the target (x, y)."""
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

    def pick(self):
        """Pick up garbage if on the same position."""
        if environment[self.x][self.y] == 'G':
            self.garbage_collected = True
            environment[self.x][self.y] = '.'
            print(f"{self.name} picked up garbage at ({self.x}, {self.y})")

    def drop(self):
        """Drop garbage at current position if holding any."""
        if self.garbage_collected:
            print(f"{self.name} dropped garbage at ({self.x}, {self.y})")
            self.garbage_collected = False

class CleaningRobot(Robot):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

class BurningRobot(Robot):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

    def burn(self):
        """Burn garbage at current position."""
        if self.pos() == R2_POSITION:
            print(f"{self.name} burned garbage at its position ({self.x}, {self.y})")

environment = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

for _ in range(5):
    gx, gy = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    environment[gx][gy] = 'G'

r1 = CleaningRobot('r1', 0, 0)  # At North West corner
r2 = BurningRobot('r2', R2_POSITION[0], R2_POSITION[1])  # At the center

def print_environment():
    """Display the environment grid."""
    for row in environment:
        print(' '.join(row))
    print()

def simulate():
    garbage_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if environment[x][y] == 'G']
    
    for gx, gy in garbage_positions:
        while r1.pos() != (gx, gy):
            r1.move_towards(gx, gy)
            print(f"{r1.name} moved to ({r1.x}, {r1.y})")

        r1.pick()

        while r1.pos() != R2_POSITION:
            r1.move_towards(R2_POSITION[0], R2_POSITION[1])
            print(f"{r1.name} moved to ({r1.x}, {r1.y})")

        r1.drop()

        r2.burn()

print("Initial Environment:")
print_environment()

simulate()

print("\nFinal Environment:")
print_environment()
