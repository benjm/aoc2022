import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()
def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

filename = sys.argv[1]
max_rocks = 1000000000000
print_rock_n = -1

if len(sys.argv)>2:
    max_rocks = int(sys.argv[2])
if len(sys.argv)>3:
    print_rock_n = int(sys.argv[3])

lines = []
with open(filename) as f:
    lines = f.read().splitlines()

# Arrrr, this was a nasty one and the code is a mess. It could use some serious refactoring.

@dataclass
class Point:
    x: int
    y: int

# rocks=["..####".split(),"...#. ..### ...#.".split(),"....# ....# ..###".split(),"..# ..# ..# ..#".split(),"..## ..##".split()]
# for rock in rocks:
#     for row in rock:
#         print(row)
#     print()

left=0
right=7
bottom_left=(2,3) # above highest
highest=0

rocks=[
    [Point(2,4),Point(3,4),Point(4,4),Point(5,4)],
    [Point(3,4),Point(2,5),Point(3,5),Point(4,5),Point(3,6)],
    [Point(2,4),Point(3,4),Point(4,4),Point(4,5),Point(4,6)],
    [Point(2,4),Point(2,5),Point(2,6),Point(2,7)],
    [Point(2,4),Point(3,4),Point(2,5),Point(3,5)]
]

base=["#######",".......",".......","......."]

RIGHT=">"
LEFT="<"
ROCK = "#"
AIR = "."
winds=list(lines[0])
print(f"There are {len(winds)} winds")
wind_i=0

def inBase(point, base):
    if len(base)<=point.y:
        return False
    row = base[point.y]
    result=True
    try:
        result = row[point.x] == ROCK
    except:
        print("ERROR?",point,row)
    return result

def oneStep(rock,base,w,prnt):
    if prnt: print("oneStep",w,rock)
    dx = [-1,1][w==">"]
    if any(((p.x+dx) < 0 or (p.x+dx) > 6) for p in rock):
        if prnt: print("no horizontal movement due to walls")
        pass
    elif any(inBase(Point(p.x+dx,p.y),base) for p in rock):
        if prnt: print("no horizontal movement due to base")
        pass
    else:
        if prnt: print("horizontal movement")
        rock = [Point(p.x+dx,p.y) for p in rock]
    if any(inBase(Point(p.x,p.y-1),base) for p in rock):
        if prnt: print("comes to rest")
        return (True,rock)
    rock = [Point(p.x,p.y-1) for p in rock]
    return (False,rock)
    #atRest,rock

def blowUntilStop(rock,base,winds,wind_i,prnt):
    atRest=False
    while not atRest:
        actual_wind_i = wind_i%len(winds)
        w = winds[actual_wind_i]
        wind_i+=1
        atRest,rock=oneStep(rock,base,w,prnt)
    if prnt: print("rock stopped",rock)
    return (rock,wind_i)

def updateBase(base,highest,rock):
    max_y = max(p.y for p in rock)
    if max_y >= highest:
        for add_air_i in range(max_y - highest):
            base.append(AIR*7)
        highest = max_y
    for p in rock:
        row = base[p.y]
        new_row = row[:p.x]+ROCK+row[p.x+1:]
        base[p.y] = new_row
    return base,highest

def printBase(base,lmt=20):
    stop=-1
    if len(base)>lmt:
        stop = len(base)-lmt-1
    for i in range(len(base)-1,stop,-1):
        row = base[i]
        if i == 0:
            row = "~"*7
        print("|"+row+"|")

print(elapsedTimeMs(),"starting part1 - day17")
# 7 units wide
# rocks enter with left edge 2 from wall and base 3 above highest
# push then fall/rest
# on rest the new rock immediately starts falling
# height after 2022 rocks have fallen

@dataclass
class Datum:
    wind_i: int
    rock_i: int
    height: int

wind_rock_height_map={}
wind_rock_repeat_map={}

for rock_i in range(max_rocks):
    rock=[Point(p.x,p.y+highest) for p in rocks[rock_i%5]]
    wind_rock_index=(wind_i%len(winds), rock_i%5)
    current_datum = Datum(wind_i, rock_i, highest)
    if wind_rock_index in wind_rock_height_map and wind_rock_index not in wind_rock_repeat_map:
        prev_datum = wind_rock_height_map[wind_rock_index]
        print(f"found a new repeat at wind_rock_index {wind_rock_index} with change from {prev_datum} to {current_datum}")
        wind_rock_repeat_map[wind_rock_index]=[prev_datum, current_datum]
    wind_rock_height_map[wind_rock_index] = current_datum
    rock,wind_i = blowUntilStop(rock,base,winds,wind_i,rock_i+1==print_rock_n)
    base,highest = updateBase(base,highest,rock)
    if rock_i%100000 == 0 : # 1 000 000 000 000
        print(elapsedTimeMs(),"ROCK",rock_i,rock,highest)
        printBase(base)
        print()

print(elapsedTimeMs(),f"HIGHEST after {max_rocks} was {highest}")
printBase(base)
print()

print(elapsedTimeMs(),"starting part2")
# 1000000000000 rocks ... the Dr Evil value ... going to have to find a pattern

# ? patterns in winds ?

def patternHunt(text):
    double_text = text*2
    l = len(text)
    for d in range(l//2,l//20,-1):
        if l%d==0:
            for i in range(l//2):
                if text[i:i+d] in double_text[i+d:]:
                    return d,text[i:i+d]
    return 0,None
# print("wind patternhunt result:\n",patternHunt(lines[0]))
# no patterns

most_rocks=0
datum_pair=[None,None]
for wri in wind_rock_repeat_map:
    prev_datum, current_datum = wind_rock_repeat_map[wri]
    rocks = current_datum.rock_i - prev_datum.rock_i
    if rocks>most_rocks:
        most_rocks=rocks
        datum_pair=[prev_datum, current_datum]
d0,d1=datum_pair
print(f"biggest repeating pattern found: {most_rocks} fall between {d0} and {d1}")
big_target=1000000000000
print(f"target is {big_target} rocks\nInitially {prev_datum.rock_i} fall before the selected repeat begins")
n_repeats = (big_target-prev_datum.rock_i)//most_rocks
height_after_nth_repeat = n_repeats * (current_datum.height - prev_datum.height) + prev_datum.height
rocks_still_to_fall = (big_target-prev_datum.rock_i)%most_rocks
print(f"after {n_repeats} repeats of the pattern the height should be {height_after_nth_repeat} with {rocks_still_to_fall} rocks_still_to_fall")

# is biggest datum delta the best option?
perfect_most_rocks=0
perfect_datum_pair=None
for wri in wind_rock_repeat_map:
    prev_datum, current_datum = wind_rock_repeat_map[wri]
    rocks = current_datum.rock_i - prev_datum.rock_i
    big_target
    if (big_target-prev_datum.rock_i)%rocks == 0:
        if rocks>perfect_most_rocks:
            perfect_most_rocks=rocks
            perfect_datum_pair=[prev_datum, current_datum]
            print(f"found perfect_datum_pair {perfect_datum_pair}")
if perfect_datum_pair:
    print("PERFECT DATUM PAIR FOUND!")
    d0,d1=perfect_datum_pair
    most_rocks=d1.rock_i-d0.rock_i
    print(f"biggest repeating pattern found: {d1.rock_i-d0.rock_i} fall between {d0} and {d1}")
    big_target=1000000000000
    print(f"target is {big_target} rocks\nInitially {d0.rock_i} fall before the selected repeat begins")
    n_repeats = (big_target-d0.rock_i)//most_rocks
    height_after_nth_repeat = n_repeats * (d1.height - d0.height) + d0.height
    rocks_still_to_fall = (big_target-d0.rock_i)%most_rocks
    print(f"after {n_repeats} repeats of the pattern the height should be {height_after_nth_repeat} with {rocks_still_to_fall} rocks_still_to_fall")
    # CORRECT! XD
    # PERFECT DATUM PAIR FOUND!
    # biggest repeating pattern found: 1720 fall between Datum(wind_i=8455, rock_i=1440, height=2286) and Datum(wind_i=18546, rock_i=3160, height=4988)
    # target is 1000000000000 rocks
    # Initially 1440 fall before the selected repeat begins
    # after 581395348 repeats of the pattern the height should be 1570930232582 with 0 rocks_still_to_fal
    # 0:00:00.193702 END
    # ...phew, no secondary fall pattern to work out
print(elapsedTimeMs(),"END")