from dataclasses import dataclass
from typing import List

@dataclass
class Letter:
    char: str
    x: int
    y: int

def day4():
    data = import_data('./data/day4.txt')
    find_xmas(data)
    count_cross(data)


def import_data(file: str) -> List[str]:
    data: List[str] = list()
    with open(file, 'r') as file:
        for line in file:
            data.append(line)

    return data


def test_letter(data: List[str], char: str, x: int, y: int) -> bool:
    if x < 0 or y < 0:
        return False
    
    if y > len(data)-1 or x > len(data[y])-1:
        return False
    
    return data[y][x] == char


def count_all(data: List[str], char: str, x: int, y:int) -> int:
    total = 0

    # Test all nearest neighbours of letter
    for i in range(-1,2,1):
        for j in range (-1,2,1):
            if find_in_line(data, char, x, y, i, j):
                total += 1
    
    return total


def find_in_line(data: List[str], char: str, x: int, y:int, xdir: int, ydir:int) -> bool:
    target = 'XMAS_'
    target_letter = target[target.find(char) + 1]
    if test_letter(data, target_letter, x+xdir, y+ydir):
        if target_letter == 'S':
            return True
        else:
            return find_in_line(data, target_letter, x+xdir, y+ydir, xdir, ydir)
    else:
        return False
    

def find_xmas(data: List[str]):
    total = 0
    for y in range(len(data)):
        for x, char in enumerate(data[y]):
            if char == 'X':
                total += count_all(data, char, x, y)

    print(f'XMAS: {total}')


def test_cross(data: List[str], x: int, y:int) -> bool:
    # Test ordinal directions
    # Combinations M-M / S-S, M-S / S-M -> Same top then same bottom, if not same then opposite

    # Test top
    if test_letter(data, 'M', x-1, y-1):
        if test_letter(data, 'M', x+1, y-1):
            if test_letter(data, 'S', x-1, y+1) and test_letter(data, 'S', x+1, y+1):
                # M-M / S-S
                return True
        elif test_letter(data, 'S', x+1, y-1):
            if test_letter(data, 'M', x-1, y+1) and test_letter(data, 'S', x+1, y+1):
                # M-S / M-S
                return True
    elif test_letter(data, 'S', x-1, y-1):
        if test_letter(data, 'S', x+1, y-1):
            if test_letter(data, 'M', x-1, y+1) and test_letter(data, 'M', x+1, y+1):
                # S-S / M-M
                return True
        elif test_letter(data, 'M', x+1, y-1):
            if test_letter(data, 'S', x-1, y+1) and test_letter(data, 'M', x+1, y+1):
                # S-M / M-S
                return True
            

def count_cross(data):
    total = 0
    for y in range(len(data)):
        for x, char in enumerate(data[y]):
            if char == 'A':
                if test_cross(data, x, y):
                    total += 1

    print(f'Cross: {total}')         


if __name__ == "__main__":
    day4()
    
