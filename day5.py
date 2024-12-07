from dataclasses import dataclass
from typing import List

@dataclass
class Rule:
    first: int
    second: int

@dataclass
class Day5Data:
    rules: List[Rule]
    updates: List[List[int]]


def day5():
    pass

def import_data(file: str) -> List[str]:
    data: List[str] = list()
    with open(file, 'r') as file:
        for line in file:
            data.append(line)

    return data

def process_rule(line: str) -> Rule:
    ruleRegex = r'(\d+)\|(\d+)'



if __name__ == "__main__":
    pass