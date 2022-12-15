from dataclasses import dataclass
import sys
import math

filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

# class MyClass:
#     def __init__(self, id):
#         self.id=id
#     def __str__(self):
#         return f"MyClass {self.id}"

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

@dataclass
class Move:
    dx: int
    dy: int
    nam: str

print("starting part1")
entry = Point(500,0)
ROCK="#"
SAND="o"
AIR="."
rocks=set()
sands=set()
solid=set()
for line in lines:
    #503,4 -> 502,4 -> 502,9 -> 494,9
    points = [*map(lambda xy:[*map(int,xy.split(","))],line.split(" -> "))]
    p=Point(points[0][0],points[0][1])
    rocks.add(p)
    solid.add(p)
    for i in range(len(points)-1):
        sx,sy = points[i]
        ex,ey = points[i+1]
        dx = [[0,-1][ex<sx],1][ex>sx]
        dy = [[0,-1][ey<sy],1][ey>sy]
        while sx!=ex or sy!=ey:
            sx+=dx
            sy+=dy
            rock=Point(sx,sy)
            rocks.add(rock)
            solid.add(rock)
nStartingRocks=len(rocks)
print("total rocks:",nStartingRocks)

lasty=max(p.y for p in rocks)

def printOut(rocks,buf,floor=False):
    #min and max with a buffer around
    lx=min(p.x for p in solid)
    rx=max(p.x for p in solid)
    ry=max(p.y for p in rocks)
    width=(2*buf)+rx-lx
    lx-=buf
    height=[buf+ry,lasty+1][floor]

    for y in range(height):
        row=[]
        for dx in range(width):
            p=Point(lx+dx, y)
            if p in rocks:
                row.append(ROCK)
            elif p in sands:
                row.append(SAND)
            elif p == entry:
                row.append("V")
            else:
                row.append(AIR)
        print(" ".join(row))
    if floor:
        print(" ".join(["#"]*width))
    print()
#printOut(rocks,3)


DN=Move(0,1,"DN")
DL=Move(-1,1,"DL")
DR=Move(1,1,"DR")

def findMove(sand):
    dn=Point(sand.x,sand.y+1)
    dl=Point(sand.x-1,sand.y+1)
    dr=Point(sand.x+1,sand.y+1)
    if dn not in solid:
        return DN
    elif dl not in solid:
        return DL
    elif dr not in solid:
        return DR
    else:
        return None

def addSand(x,y):
    sand = Point(x,y)
    move = findMove(sand)
    while move and sand.y<lasty:
        sand = Point(sand.x+move.dx,sand.y+move.dy)
        move = findMove(sand)
    return sand

def pourSand():
    sand = addSand(entry.x,entry.y)
    while 0 < sand.y <= lasty:
        sands.add(sand)
        solid.add(sand)
        sand = addSand(entry.x,entry.y)
        if len(sands)%100==0:
            print("added",len(sands),"...so far")
    if sand == entry:
        sands.add(sand)
        solid.add(sand)
    print("Finished Pouring",sand)

pourSand()
printOut(rocks,3)
print("PART1:",len(sands),len(solid)-nStartingRocks)

print("starting part2")

solid = set()
sands = set()
for rock in rocks:
    solid.add(rock)
lasty+=1
pourSand()
printOut(rocks,3,True)
print("PART2:",len(sands),len(solid)-nStartingRocks)

