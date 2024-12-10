from dataclasses import dataclass
from typing import List, Dict
import time
@dataclass
class Expression:
    result: int
    args: List[int]

class Day7:
    def __init__(self):
        self.filePath = './data/day7.txt'
        self.expressions: List[Expression] = list()

    def import_data(self):
        with open(self.filePath, 'r') as file:
            for line in file:
                self.process_line(line)
    

    def process_line(self, line: str) -> Expression:
        line = line.strip()
        parts = line.split(':')
        result = int(parts[0])
        args = [int(n) for n in parts[1].strip().split()]
        exp = Expression(result, args)
        self.expressions.append(exp)
        return exp
    

    def eval_expressions(self, part2: bool = False):
        total = 0
        logGood = True
        for i, e in enumerate(self.expressions):
            if part2:
                if  self.compute_expression(e) or self.compute_expression2(e):
                    total += e.result
                    if logGood: print(f'Compute: {e.result}')
            elif self.compute_expression(e):
                total += e.result
                if logGood: print(f'Compute: {e.result}')

        print(f'Total: {total}')


    def compute_expression(self, exp: Expression) -> bool:
        opField = 0b0
        maxOp = 0
        for i in range(len(exp.args) - 1):
            maxOp = maxOp << 1 | 0b1

        while opField <= maxOp:
            if self.test_expression(exp, opField):
                return True
            
            opField += 1

        return False


    def test_expression(self, exp: Expression, opField: int) -> bool:
        args = exp.args.copy()
        opFieldShift = opField

        result = args.pop(0)
        for i in range(len(args)):
            x = args.pop(0)
            isMult = 0b1 & opFieldShift > 0
            result = result * x if isMult else result + x
            if result > exp.result:
                return False
            opFieldShift = opFieldShift >> 1
        
        return result == exp.result

    def compute_expression2(self, exp: Expression) -> bool:
        opField: List[str] = list()
        for i in range(len(exp.args) - 1):
            opField.append('+')

        while opField is not None:
            if self.test_expression2(exp, opField):
                print(f'{exp.result} -> {opField}')
                return True
            
            opField = self.get_next_opField(opField)

        return False

    def test_expression2(self, exp: Expression, opField: List[str]) -> bool:
        args = exp.args.copy()
        ops = opField.copy()

        argA = args.pop(0)
        result: int
        for i in range(len(args)):
            argB = args.pop(0)
            op = ops.pop(0)
            if op == '+':
                result = argA + argB
            elif op == '*':
                result = argA * argB
            elif op == '|':
                result = int(str(argA) + str(argB))

            if result > exp.result:
                return False
            argA = result
        
        return result == exp.result        


    def get_next_opField(self, opField: List[str]) -> List[str]:
        carry = True
        newOp: List[str] = list()
        for i in range(len(opField)):
            if carry:
                op = self.get_next_op(opField[i])
                newOp.append(op)
                carry = True if op == '+' else False
            else:
                newOp.append(opField[i])

        if '|' not in newOp and '*' not in newOp:
            return None

        return newOp


    def get_next_op(self, char: str) -> str:
        chars = '+*|+'
        i = chars.find(char)
        return chars[i+1]


if __name__ == '__main__':
    t = Day7()
    t.import_data()
    t.eval_expressions(True)