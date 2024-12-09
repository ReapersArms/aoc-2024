from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Point:
    x: int
    y: int
    isObstacle: bool = False
    isTraversed: bool = False
    travelDirections: str = ''

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
    route: List[Point] = list()
    loops: int = 0

    newPos = guard.pos
    newPos.travelDirections = guard.dir
    route.append(newPos)
    #route.append(guard.pos)
    while not guard.gone:
        if detect_route(grid, route, guard):
            loops += 1
        guard = get_next_pos(grid, guard)

        for p in route:
            if p.x == guard.pos.x and p.y == guard.pos.y:
                break
        else:
            newPos = guard.pos
            newPos.travelDirections = guard.dir
            route.append(newPos)
        # if guard.pos not in route:
        #     route.append(guard.pos)

    print(f'Route: {len(route)}')
    print(f'Loops: {loops}')
    return route

# def insert_obstacle(grid: Grid, point: Point):
#     point.isObstacle = True
#     grid.poi.append(point)

def detect_route(grid: Grid, routes: List[Point], guard: Guard) -> bool:
    # Test if there is a unblocked route on right of the current path
    validRoutes: List[Point] = list()
    validRoutes.extend(grid.poi)
    validRoutes.extend(routes)
    nearestPoint: Point = None
    points: Dict[str, Point] = {
        'north': None,
        'south': None,
        'east': None,
        'west': None,
        'obst': None,
    }
    
    if guard.dir == 'north':
        # Filter all routes on same y
        validRoutes = [p for p in validRoutes if p.y == guard.pos.y]
        # Filter all routes where x is less than current
        validRoutes = [p for p in validRoutes if p.x > guard.pos.x]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle or 'east' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.x < nearestPoint.x:
                    nearestPoint = p
    elif guard.dir == 'south':
        # Filter all routes on same y
        validRoutes = [p for p in validRoutes if p.y == guard.pos.y]
        # Filter all routes where x is greater than current
        validRoutes = [p for p in validRoutes if p.x < guard.pos.x]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle or 'west' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.x > nearestPoint.x:
                    nearestPoint = p
    elif guard.dir == 'east':
        # Filter all routes on same y
        validRoutes = [p for p in validRoutes if p.x == guard.pos.x]
        # Filter all routes where y is less than current
        validRoutes = [p for p in validRoutes if p.y > guard.pos.y]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle or 'south' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.y < nearestPoint.y:
                    nearestPoint = p
    elif guard.dir == 'west':
        # Filter all routes on same x
        validRoutes = [p for p in validRoutes if p.x == guard.pos.x]
        # Filter all routes where y is less than current
        validRoutes = [p for p in validRoutes if p.y < guard.pos.y]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle or 'north' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.y > nearestPoint.y:
                    nearestPoint = p

    if nearestPoint is None or nearestPoint.isObstacle:
        return False

    #print(f'Nearest: {nearestPoint}')
    return True


if __name__ == "__main__":
    day6()
