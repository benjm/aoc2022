import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("DAY 12: starting part1")

class MyClass:
    def __init__(self, id):
        self.id=id
    def __str__(self):
        return f"MyClass {self.id}"

def toId(x,y):
    return str(x)+","+str(y)
def fromId(id):
    return map(int,id.split(","))

height = len(lines)
width = len(lines[0])
weights = {}
start=end=None
for y in range(height):
    for x in range(width):
        id = toId(x,y)
        weights[id] = math.inf
        v = lines[y][x]
        if v=="S":
            start = id
            weights[id] = 0
        elif v=="E":
            end = id

visited=set()
edge=set()
edge.add(start)
steps=0

def ordVal(c):
    if c=="S":
        return ord("a")
    if c=="E":
        return ord("z")
    return ord(c)

def canMoveTo(a,b,x,y):
    return (x>=0 and x<width) and (y>=0 and y<height) and (toId(x,y) not in visited) and (ordVal(lines[y][x]) <= ordVal(lines[b][a]) +1)


while end not in edge:
    steps+=1
    newEdge=set()
    visited.update(edge)
    for id in edge:
        x,y = fromId(id)
        if canMoveTo(x,y,x-1,y):
            newEdge.add(toId(x-1,y))
        if canMoveTo(x,y,x+1,y):
            newEdge.add(toId(x+1,y))
        if canMoveTo(x,y,x,y-1):
            newEdge.add(toId(x,y-1))
        if canMoveTo(x,y,x,y+1):
            newEdge.add(toId(x,y+1))
    edge=newEdge
    for id in edge:
        weights[id]=steps


print("steps taken to reach end:",steps)
