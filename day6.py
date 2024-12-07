from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    x: int
    y: int
    isObstacle: bool = False
    isTraversed: bool = False

@dataclass
class Guard:
    pos: Point
    dir: str
    gone: bool

@dataclass
class Grid:
    poi: List[Point]
    maxX: int
    maxY: int

def day6():
    data = import_data('./data/day6.txt')
    guard = get_initial_guard(data)
    points = patrol(data, guard)
    print(len(points))

def import_data(file: str) -> Grid:
    grid = Grid(list(), 0, 0)
    points = list()
    with open(file, 'r') as file:
        for i, line in enumerate(file):
            line = line.strip()
            newPoints = find_points_of_interest(i, line)
            points.extend(newPoints)
            grid.maxY = i
            grid.maxX = len(line)

    grid.poi = points
    return grid


def find_points_of_interest(y: int, line: str) -> List[Point]:
    points = list()
    for x, char in enumerate(line):
        if char == '#':
            points.append(Point(x, y, True, False))
        elif char != '.':
            points.append(Point(x, y, False, True))

    return points

def safe_to_traverse(grid: Grid, nextPos: Point):
    if nextPos.x > grid.maxX or nextPos.y > grid.maxY:
        return None
    elif nextPos.x < 0 or nextPos.y < 0:
        return None

    for p in grid.poi:
        if p.x == nextPos.x and p.y == nextPos.y:
            return not p.isObstacle
        
    return True

def get_next_pos(grid: Grid, guard: Guard) -> Guard:
    while True:
        nextPos = get_next_point(guard)
        safe = safe_to_traverse(grid, nextPos)
        if safe is None:
            guard.gone = True
            return guard
        if safe == True:
            guard.pos = nextPos
            return guard
        
        # else change direction and try again
        guard.dir = turn_90(guard.dir)


def get_next_point(guard: Guard) -> Point:
    if guard.dir == 'north':
        return Point(guard.pos.x, guard.pos.y - 1)
    elif guard.dir == 'south':
        return Point(guard.pos.x, guard.pos.y + 1)
    elif guard.dir == 'west':
        return Point(guard.pos.x - 1, guard.pos.y)
    elif guard.dir == 'east':
        return Point(guard.pos.x + 1, guard.pos.y)
    
def turn_90(direction: str) -> str:
    if direction == 'north':
        return 'east'
    elif direction == 'east':
        return 'south'
    elif direction == 'south':
        return 'west'
    elif direction == 'west':
        return 'north'
    
def get_initial_guard(grid: Grid) -> Guard:
    for p in grid.poi:
        if p.isTraversed:
            return Guard(p, 'north', False)
        
    return None

def patrol(grid: Grid, guard: Guard) -> List[Point]:
    route = list()
    route.append(guard.pos)
    while not guard.gone:
        guard = get_next_pos(grid, guard)
        if guard.pos not in route:
            route.append(guard.pos)

    return route
    



if __name__ == "__main__":
    day6()
