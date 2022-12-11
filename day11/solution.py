import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3
class Monkey:
    reducer = 0
    def __init__(self, id, items, operation, divisor, if_true, if_false):
        self.id=id
        self.items=items
        self.operation=operation
        self.divisor=divisor
        self.if_true=if_true
        self.if_false=if_false
        self.inspected=0
    def __str__(self):
        return f"Monkey {self.id} ({self.inspected}): {self.items}"
    def thrown(self, item):
        self.items.append(item)
    def takeTurn(self, monkeys):
        self.inspected+=len(self.items)
        temp = self.items
        self.items = []
        for old in temp:
            s=str(old)+self.operation[0]+self.operation[1]
            new = eval(s)
            if reducer > 0:
                new %= self.reducer
            else:
                new //= 3
            recipient = [self.if_false,self.if_true][new % self.divisor == 0]
            #print(f"Monkey {self.id} func: {s} and so {old}-->{new} and so {self.id}-->{recipient}")
            monkeys[recipient].thrown(new)

monkeys={}
divisors=set()
for i in range(0,len(lines),7):
    id = int(lines[i][:-1].split()[1])
    items = [*map(int,lines[i+1].split(": ")[1].split(", "))]
    operation = lines[i+2].split()[-2:]
    divisor = int(lines[i+3].split()[-1])
    if_true = int(lines[i+4].split()[-1])
    if_false = int(lines[i+5].split()[-1])
    monkeys[id] = Monkey(id,items,operation,divisor,if_true,if_false)
    divisors.add(divisor)

# set divisor based on all monkeys
reducer = math.lcm(*divisors)
for id in monkeys:
    monkeys[id].reducer = reducer
print(f"reducing by {reducer} ...")

rounds = 10000
for r in range(rounds):
    if r%1000 == 0:
        print(f"starting round {r}")
    for id in sorted(monkeys):
        monkey = monkeys[id]
        monkey.takeTurn(monkeys)
print(f"after {rounds} rounds:")
for id in monkeys:
    print(monkeys[id])
print("top two multiplied:",math.prod(sorted(monkeys[id].inspected for id in monkeys)[-2:]))

print("starting part2")
#re-use the above with 

