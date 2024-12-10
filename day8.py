from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class Point:
    x: int
    y: int
    freq: str = ''
    node: bool = False

class Day8:
    def __init__(self):
        self.filePath = './data/day8.txt'
        self.freqs: List[str] = list()
        self.maxX: int = 0
        self.maxY: int = 0
        self.grid: Dict[int, Dict[int, Point]] = {}
        self.towers: Dict[str, List[Point]] = {}
        self.nodes: List[Point] = list()
        

    def import_data(self):
        with open(self.filePath, 'r') as file:
            i = 0
            for line in file:
                self.maxY = i if i > self.maxY else self.maxY
                self.process_line(i, line)
                i += 1
    

    def process_line(self, y: int, line: str):
        line = line.strip()
        for x, c in enumerate(line):
            self.maxX = x if x > self.maxX else self.maxX
            if c == '.':
                continue
            if c not in self.freqs:
                self.freqs.append(c)
                self.towers[c] = list()
            self.add_tower(x, y, c)

    def add_to_grid(self, p: Point):
        if self.grid.get(p.x) is None:
            self.grid[p.x] = {}

        self.grid[p.x][p.y] = p

    def add_tower(self, x: int, y:int, freq: str):
        if self.grid.get(x) is None or self.grid[x].get(y) is None:
            p = Point(x, y, freq=freq)
            self.add_to_grid(p)
            if self.towers.get(freq) is None:
                self.towers[freq] = list()
            self.towers[freq].append(p)
            
        else:
            self.grid[x][y].freq = freq

    def add_node(self, x: int, y:int):
        if self.grid.get(x) is None or self.grid[x].get(y) is None:
            p = Point(x, y, node=True)
            self.add_to_grid(p)
            self.nodes.append(p)
        else:
            p = self.grid[x][y]
            if not p.node:
                p.node = True
                self.nodes.append(p)

    def calculate_nodes(self, p1: Point, p2: Point, resonant: bool = False) -> List[Point]:
        nodes: List[Point] = list()
        if resonant: nodes.append(p1)
        x = p1.x - p2.x
        y = p1.y - p2.y
        nodeX = p1.x + x
        nodeY = p1.y + y
        while not (nodeX > self.maxX or nodeY > self.maxY or nodeX < 0 or nodeY < 0):
            nodes.append(Point(nodeX, nodeY, node=True))
            if not resonant:
                return nodes
            else:
                nodeX += x
                nodeY += y

        return nodes
    
    def generate_nodes(self, resonant: bool = False):
        for freq in self.freqs:
            # Iterate main tower
            for i in range(len(self.towers[freq])):
                towers = self.towers[freq].copy()
                p1 = towers.pop(i)
                # Iterate over remaining towers
                for p2 in towers:
                    nodes = self.calculate_nodes(p1, p2, resonant=resonant)
                    if len(nodes) > 0:
                        for node in nodes:
                            self.add_node(node.x, node.y)
    
if __name__ == "__main__":
    t = Day8()
    t.import_data()
    t.generate_nodes(True)
    print(len(t.nodes))
    pass