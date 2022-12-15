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

class Path:
    def __init__(self, path):
        self.path=[]
        for node in path:
            self.path.append(node)
    def step(self,node):
        return Path(self.path+[node])
    def end(self):
        if len(self.path)<1:
            return None
        return self.path[-1]
    def __str__(self):
        return f"Path {len(self.path)}:{str(self.end())}"

class Node:
    def toId(x,y):return "("+str(x)+","+str(y)+")"
    def __init__(self, x, y, val, w, h):
        self.x=x
        self.y=y
        self.id=Node.toId(x,y)
        if val=="S":
            val=chr(ord("a"))
        elif val=="E":
            val=chr(ord("z"))
        self.val=val
        self.neighbourIds=[]
        for nx in [x-1,x+1]:
            if nx>=0 and nx<width:
                self.neighbourIds.append(Node.toId(nx,y))
        for ny in [y-1,y+1]:
            if ny>=0 and ny<height:
                self.neighbourIds.append(Node.toId(x,ny))
        self.getToFromIds=set()
    def checkAccess(self, nodes):
        for id in self.neighbourIds:
            neighbour=nodes[id]
            if ord(neighbour.val) >= ord(self.val)-1:
                self.getToFromIds.add(id)
    def __str__(self):
        return f"Node {self.id} ({self.val})"

height = len(lines)
width = len(lines[0])
nodes={}
start=end=None
for y in range(height):
    for x in range(width):
        v = lines[y][x]
        node = Node(x,y,v, width, height)
        nodes[node.id]=node
        if v=="S":
            start = node
        elif v=="E":
            end = node
print(start,"to",end)
for id in sorted(nodes):
    nodes[id].checkAccess(nodes)
    # if len(nodes[id].neighbourIds) != len(nodes[id].getToFromIds):
    #     print(nodes[id],nodes[id].getToFromIds)

currentSearch=set()
currentSearch.add(Path([end]))
been=set()
been.add(end.id)
steps=0
earlyA = False

while start.id not in been and len(currentSearch)>0:
    #print(f"{steps}: {[*map(str,currentSearch)]}")
    steps+=1
    nextSearch=set()
    for path in currentSearch:
        end = path.end()
        for id in end.getToFromIds:
            if id not in been:
                stepTo = nodes[id]
                newpath = path.step(stepTo)
                nextSearch.add(newpath)
                been.add(id)
                if not earlyA and stepTo.val == "a":
                    earlyA = True
                    print("FIRST a found within",steps,"steps")
                    print("FIRST a found within",steps,"steps")
                    print("FIRST a found within",steps,"steps")
    currentSearch=nextSearch

if start.id not in been:
    print("ERROR - finished without reaching end")

# 1st try was wrong - 470 was too high

for path in currentSearch:
    idPath = [node.id for node in path.path]
    if start.id in idPath:
        for y in range(height):
            row=[]
            for x in range(width):
                c = lines[y][x]
                if Node.toId(x,y) in idPath:
                    row+=[c.upper()]
                else:
                    row+=[c]
            print(" ".join(row))
        print(f"path from S to E took {steps}")
        print("".join(node.val for node in path.path)[::-1])


print("starting part2")

