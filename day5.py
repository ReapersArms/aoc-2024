from dataclasses import dataclass
from typing import List
import re

@dataclass
class Rule:
    first: int
    second: int

@dataclass
class Day5Data:
    rules: List[Rule]
    updates: List[List[int]]


def day5():
    data = import_data('./data/day5.txt')
    process_data(data)

def import_data(file: str) -> List[str]:
    data: Day5Data = Day5Data(list(), list())
    with open(file, 'r') as file:
        for line in file:
            entry = process_rule(line)
            if entry is not None:
                data.rules.append(entry)
                continue
            
            entry = process_revisions(line)
            if entry is not None:
                data.updates.append(entry)

    return data

def process_rule(line: str) -> Rule:
    rulePattern = r'(\d+)\|(\d+)'
    match = re.match(rulePattern, line)
    if (match):
        return Rule(
            int(match.group(1)), 
            int(match.group(2))
        )
    
    return None

def process_revisions(line: str) -> List[int]:
    nums = list()
    revisionPattern = r'(\d+,?)+'
    if re.match(revisionPattern, line):
        numStr = line.split(',')
        for num in numStr:
            nums.append(int(num))
    else:
        return None

    return nums


def find_relevant_rules_for_revisions(rules: List[Rule], revisions: List[int]) -> List[Rule]:
    subRules: List[Rule] = list()
    for page in revisions:
        for rule in rules:
            if rule.first == page or rule.second == page:
                subRules.append(rule)
    
    return subRules

def test_rules(pages: List[int], rules: List[Rule]):
    # For each page
    # Test all rules where page appears first, and verify previous numbers don't appear
    # Test all rules where page appears second, and verify following numbers don't appear
    for i, page in enumerate(pages):
        for rule in rules:
            # page comes first, pages with lower index should not come second
            if rule.first == page and rule.second in pages and pages.index(rule.second) < i:
                return rule
            
            # pages comes second, pages with higher index should not come first
            if rule.second == page and rule.first in pages and pages.index(rule.first) > i:
                return rule
            
    return True

def get_mid(revisions: List[int]) -> int:
    mid = int(len(revisions) / 2 -0.5)
    return revisions[mid]

def process_data(data: Day5Data):
    goodTotal = 0
    fixedTotal = 0
    for line in data.updates:
        rules = find_relevant_rules_for_revisions(data.rules, line)
        if test_rules(line, rules) == True:
            goodTotal += get_mid(line)
        else:
            newLine = try_fix_revision(line, rules)
            fixedTotal += get_mid(newLine)

    print(f'Good Total: {goodTotal}')
    print(f'Fixed Total: {fixedTotal}')


def try_fix_revision(revisions: List[int], rules: List[Rule]) -> List[int]:
    newOrder = revisions.copy()
    while True:
        result = test_rules(newOrder, rules)
        if result == True:
            return newOrder
        
        # Use result to fix list
        # Put second next to first
        first_index = newOrder.index(result.first)
        newOrder.remove(result.second)
        newOrder.insert(first_index+1, result.second)


if __name__ == "__main__":
    day5()