import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

EDGE="#"
SPACE="."
RIGHT=">"
LEFT="<"
UP="^"
DOWN="v"
WAIT="x"
DELTAS={
    LEFT:[-1,0],
    RIGHT:[1,0],
    UP:[0,-1],
    DOWN:[0,1],
    WAIT:[0,0]
}

print_level=0
if len(sys.argv)>2:
    print_level = int(sys.argv[2])

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

@dataclass
class WindMap:
    height: int
    width: int
    edges: set
    left: dict
    right: dict
    up: dict
    down: dict
    start: Point
    target: Point

def addOrCreateSet(m,k,v):
    s=m.get(k,set())
    s.add(v)
    m[k]=s

def processLines(lines):
    height=len(lines)
    width=len(lines[0])
    wind_lcm=math.lcm(width-2,height-2)
    print(f"height {height} by width {width} repeating every {wind_lcm} rounds after ignoring edges")
    # 12 rounds for test
    # 600 rounds for input
    edges=set()
    left={}
    right={}
    up={}
    down={}
    for y in range(height):
        line = lines[y]
        for x in range(width):
            c = line[x]
            point = Point(x,y)
            s = set()
            if c == EDGE:
                edges.add(point)
            elif c == UP:
                addOrCreateSet(up,x,point)
            elif c == DOWN:
                addOrCreateSet(down,x,point)
            elif c == LEFT:
                addOrCreateSet(left,y,point)
            elif c == RIGHT:
                addOrCreateSet(right,y,point)

    # need four sets of winds: left, right, up, down
    # paths: track ends
    # each turn check possible moves from end points (remember wait is an option too)
    # end points as a set to ignore overlapping
    # until exit is possible

    start=Point(1,0)
    target=Point(width-2, height-1)
    return WindMap(height, width, edges, left, right, up, down, start, target)

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

def printTheMap(windMap, turn, new_paths):
    print("WIND MAP AT TURN",turn)
    for y in range(windMap.height):
        row=""
        for x in range(windMap.width):
            point = Point(x,y)
            if point in new_paths:
                row+="E"
            elif point == windMap.start:
                row+="S"
            elif point == windMap.target:
                row+="T"
            elif x==0 or y==0 or x==windMap.width-1 or y==windMap.height-1:
                row+=EDGE
            else:
                windy,w=windAt(windMap, turn, point)
                row+=w
        print(row)
    print()

def traverse(windMap, start_turn=0, print_level=0):
    turn=start_turn
    paths = set()
    paths.add(windMap.start)
    targetReached = False
    printTheMap(windMap,turn, paths)
    while not targetReached and len(paths)>0:
        turn+=1
        if turn%100==0:
            print(elapsedTimeMs(),"TURN",turn)
        maybe_new_paths=set()
        for path in paths:
            for dx,dy in DELTAS.values():
                point = Point(path.x+dx, path.y+dy)
                if point == windMap.target:
                    targetReached = True
                if point == windMap.target or point == windMap.start or (0<point.x<windMap.width-1 and 0<point.y<windMap.height-1):
                    maybe_new_paths.add(point)
        new_paths = checkPossible(windMap, turn, maybe_new_paths)
        if len(new_paths) == 0 :
            new_paths.add(windMap.start) # equivalent to waiting in the start locaiton until this turn
        if print_level>0:
            print("turn",turn,"went\nfrom\t",paths,"\nto\t",new_paths)
            printTheMap(windMap,turn,new_paths)
        paths = new_paths
    return turn

def checkPossible(windMap, turn, maybe_new_paths):
    paths = set()
    # scan winds in maybe points at turn
    for point in maybe_new_paths:
        windy,w=windAt(windMap, turn, point)
        if not windy:
            paths.add(point)
    return paths

#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#

def correctPoint(start_value, maximum):
    # full range 0 - max includes two walls
    value = start_value
    dist = maximum - 2
    while value < 1:
        value+=dist
    while value > maximum-2:
        value-=dist
    #print(f"{start_value} corrected to {value} based on maximum {maximum} and dist {dist}")
    return value

def windAt(windMap, turns, point):
    # left wind will have travelled turn spaces left, equivalent to point going turn spaces right
    result = False
    w=""
    point_left=Point(correctPoint(point.x+turns, windMap.width), point.y)
    point_right=Point(correctPoint(point.x-turns, windMap.width), point.y)
    point_up=Point(point.x, correctPoint(point.y+turns, windMap.height))
    point_down=Point(point.x, correctPoint(point.y-turns, windMap.height))
    #print(f"REVERSING {point} by {turns} turns resulted in: {[point_left, point_right, point_up, point_down]}")
    if point_left in windMap.left.get(point.y,set()):
        w+=LEFT
        result = True
    if point_right in windMap.right.get(point.y,set()):
        w+=RIGHT
        result = True
    if point_up in windMap.up.get(point.x,set()):
        w+=UP
        result = True
    if point_down in windMap.down.get(point.x,set()):
        w+=DOWN
        result = True
    if len(w)>1:
        w=str(len(w))
    elif len(w)<1:
        w="."
    return result,w
print(elapsedTimeMs(),"starting part1")

windMap = readFile()

steps = traverse(windMap, 0, print_level)
print(f"{elapsedTimeMs()} ==> {steps} steps taken to go from {windMap.start} to {windMap.target}")

#first attempt ... 267 is too low
#second attempt ... 292 is too low ... and the right answer for someone else
# 314 is correct! (more off by one errors ... this needs more granualar tests!)

print(elapsedTimeMs(),"starting part2")
actual_start = windMap.start
actual_target = windMap.target

windMap.start = actual_target
windMap.target = actual_start
steps_a=steps
steps=traverse(windMap, steps, print_level)
steps_b=steps-steps_a

print(f"{elapsedTimeMs()} ==> {steps} steps taken to go there and back again")
windMap.start = actual_start
windMap.target = actual_target
steps=traverse(windMap, steps, print_level)
steps_c=steps-steps_a-steps_b

print(f"{elapsedTimeMs()} ==> {steps} steps taken to go there ({steps_a}), back ({steps_b}) and there again ({steps_c})")
