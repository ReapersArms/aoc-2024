from dataclasses import dataclass
from typing import List, Dict
from copy import copy

@dataclass
class Point:
    x: int
    y: int
    isObstacle: bool = False
    isTraversed: bool = False
    #travelDirections: str = ''

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
    poiDict: Dict[int, Dict[int, Point]]

start: Point

def day6():
    data = import_data('./data/day6.txt')
    # guard = get_initial_guard(data)
    # points = patrol(data, guard)
    count_loops(data)

def import_data(file: str) -> Grid:
    grid = Grid(list(), 0, 0, dict())
    points = list()
    with open(file, 'r') as file:
        for i, line in enumerate(file):
            line = line.strip()
            newPoints = find_points_of_interest(i, line)
            points.extend(newPoints)
            grid.maxY = i
            grid.maxX = len(line) -1

    grid.poi = points
    return grid

def get_grid_dict(grid: Grid):
    grid.poiDict = {}
    for p in grid.poi:
        if grid.poiDict.get(p.x) is None:
            grid.poiDict[p.x] = {}
        grid.poiDict[p.x][p.y] = p


def find_points_of_interest(y: int, line: str) -> List[Point]:
    points = list()
    for x, char in enumerate(line):
        if char == '#':
            points.append(Point(x, y, True, False))
        elif char != '.':
            global start
            start = Point(x, y, False, True)
            points.append(Point(x, y, False, True))

    return points

def safe_to_traverse(grid: Grid, nextPos: Point):
    if nextPos.x > grid.maxX or nextPos.y > grid.maxY:
        return None
    elif nextPos.x < 0 or nextPos.y < 0:
        return None

    if grid.poiDict.get(nextPos.x) is not None:
        p = grid.poiDict[nextPos.x].get(nextPos.y)
        if p is not None:
            return not p.isObstacle
            
    # for p in grid.poi:
    #     if p.x == nextPos.x and p.y == nextPos.y:
    #         return not p.isObstacle
        
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
    global start
    return Guard(start, 'north', False)
    # for p in grid.poi:
    #     if p.isTraversed:
    #         return Guard(p, 'north', False)
        
    return None

def patrol(grid: Grid, guard: Guard) -> List[Point]:
    route: List[Point] = list()
    routeDict: Dict[int, Dict[int, Point]] = {}
    # loops: int = 0
    loop_detect = LoopDetector()

    newPos = copy(guard.pos)
    newPos.isTraversed = False
    #newPos.travelDirections = guard.dir
    route.append(newPos)
    routeDict[newPos.x] = {}
    routeDict[newPos.x][newPos.y] = newPos
    #route.append(guard.pos)
    while not guard.gone:
        # if detect_route(grid, route, guard):
        #     loops += 1
        guard = get_next_pos(grid, guard)
        if loop_detect.detect_loop(route, guard.pos):
            return 'loop'

        if routeDict.get(guard.pos.x) and routeDict[guard.pos.x].get(guard.pos.y):
            continue
        # for p in route:
        #     if p.x == guard.pos.x and p.y == guard.pos.y:
        #         break
        else:
            newPos = copy(guard.pos)
            #newPos.travelDirections = guard.dir
            route.append(newPos)
            if routeDict.get(newPos.x) is None:
                routeDict[newPos.x] = {}
            routeDict[newPos.x][newPos.y] = newPos
        # if guard.pos not in route:
        #     route.append(guard.pos)

    #print(f'Route: {len(route)}')
    # print(f'Loops: {loops}')
    return route

# def insert_obstacle(grid: Grid, point: Point):
#     point.isObstacle = True
#     grid.poi.append(point)

# def detect_route(grid: Grid, routes: List[Point], guard: Guard) -> bool:
    # Test if there is a unblocked route on right of the current path
    validRoutes: List[Point] = list()
    validRoutes.extend(grid.poi)
    validRoutes.extend(routes)
    nearestPoint: Point = None
    nearestObst: Point = None
    nearestReverse: Point = None
    
    if guard.dir == 'north':
        # Filter all routes on same y
        validRoutes = [p for p in validRoutes if p.y == guard.pos.y]
        # Filter all routes where x is less than current
        validRoutes = [p for p in validRoutes if p.x > guard.pos.x]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle:
                if nearestObst is None or p.x < nearestObst.x:
                    nearestObst = p
            if p.isObstacle or 'east' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.x < nearestPoint.x:
                    nearestPoint = p
            if 'south' in p.travelDirections:
                if nearestReverse is None or p.x < nearestReverse.x:
                    nearestReverse = p
    elif guard.dir == 'south':
        # Filter all routes on same y
        validRoutes = [p for p in validRoutes if p.y == guard.pos.y]
        # Filter all routes where x is greater than current
        validRoutes = [p for p in validRoutes if p.x < guard.pos.x]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle:
                if nearestObst is None or p.x > nearestObst.x:
                    nearestObst = p
            if p.isObstacle or 'west' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.x > nearestPoint.x:
                    nearestPoint = p
            if 'north' in p.travelDirections:
                if nearestReverse is None or p.x > nearestReverse.x:
                    nearestReverse = p
    elif guard.dir == 'east':
        # Filter all routes on same y
        validRoutes = [p for p in validRoutes if p.x == guard.pos.x]
        # Filter all routes where y is less than current
        validRoutes = [p for p in validRoutes if p.y > guard.pos.y]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle:
                if nearestObst is None or p.y < nearestObst.y:
                    nearestObst = p
            if p.isObstacle or 'south' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.y < nearestPoint.y:
                    nearestPoint = p
            if 'west' in p.travelDirections:
                if nearestReverse is None or p.y < nearestReverse.y:
                    nearestReverse = p
    elif guard.dir == 'west':
        # Filter all routes on same x
        validRoutes = [p for p in validRoutes if p.x == guard.pos.x]
        # Filter all routes where y is less than current
        validRoutes = [p for p in validRoutes if p.y < guard.pos.y]
        # Find nearest point going east that isn't blocked            
        for p in validRoutes:
            if p.isObstacle:
                if nearestObst is None or p.y > nearestObst.y:
                    nearestObst = p
            if p.isObstacle or 'north' in p.travelDirections:
                if nearestPoint is None:
                    nearestPoint = p
                elif p.y > nearestPoint.y:
                    nearestPoint = p
            if 'east' in p.travelDirections:
                if nearestReverse is None or p.y > nearestReverse.y:
                    nearestReverse = p

    if nearestPoint is None:
        return None
    
    if nearestPoint.isObstacle:
        # Check for reverse path
        if nearestReverse is None:
            return False
        
        if guard.dir == 'north' and nearestReverse.x == nearestObst.x -1:
            return True
        if guard.dir == 'south' and nearestReverse.x == nearestObst.x +1:
            return True
        if guard.dir == 'east' and nearestReverse.y == nearestObst.y -1:
            return True
        if guard.dir == 'west' and nearestReverse.y == nearestObst.y +1:
            return True

        return False                  

    #print(f'Nearest: {nearestPoint}')
    return True



# Possible strategy
# Get all spots on route
# Iterate over each and put an obstable there
# Detect if guard gets stuck in loop
#  - detect first repeat block he travels on
#  - detect when he hits that block again
def count_loops(grid: Grid):
    count = 0
    get_grid_dict(grid)
    # Get initial route
    guard = get_initial_guard(grid)
    # startingPoint = guard.pos
    initialRoute = patrol(grid, guard)
    print(f'Initial Route: {len(initialRoute)}')
    initialRoute.pop(0)
    initialPoi = grid.poi.copy()
    
    for i, p in enumerate(initialRoute):
        print(f'Test {i}')
        # Setup new grid
        grid.poi = initialPoi.copy()
        p.isObstacle = True
        grid.poi.append(p)
        get_grid_dict(grid)

        guard = get_initial_guard(grid)
        if patrol(grid, guard) == 'loop':
            print(f'Loop on {i}')
            count += 1

    print(f'Loops: {count}')


class LoopDetector:
    def __init__(self):
        self.cross: Point = None

    def detect_loop(self, route: List[Point], pos: Point) -> bool:
        if pos in route:
            if self.cross is None:
                self.cross = pos
                return False
            elif self.cross == pos:
                return True
        else:
            self.cross = None
            return False



if __name__ == "__main__":
    day6()
