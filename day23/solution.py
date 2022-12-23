import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()
def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

print_level=0
number_of_turns=10
if len(sys.argv) > 2:
    number_of_turns=int(sys.argv[2])
if len(sys.argv) > 3:
    print_level=int(sys.argv[3])

@dataclass
class Direction:
    name: str
    check: list

@dataclass(unsafe_hash=True)
class Elf:
    x: int
    y: int
    def nextTo(self, other):
        x_by_one = abs(self.x-other.x)
        y_by_one = abs(self.y-other.y)
        return max([x_by_one,y_by_one])==1

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    elves = []
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            c = line[x]
            if c == "#":
                elf = Elf(x,y)
                elves.append(elf)
    return elves

elves = readFile()
ELF="#"
SPACE="."
NORTH=Direction("north",[[-1,-1],[0,-1],[1,-1]])
SOUTH=Direction("south",[[-1,1], [0, 1],[1, 1]])
WEST =Direction("west", [[-1,-1],[-1,0],[-1,1]])
EAST =Direction("east", [[1,-1], [1, 0],[1, 1]])
ALL_DELTAS=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]

print(elapsedTimeMs(),"starting part1 - day 23")

def printTheElves(elves,border=2):
    border+=1
    rect = getRectangle(elves)
    x0,y0,x1,y1 = rect
    print(rect)

    row="y\\x".rjust(5)+" "
    for x in range(x0-border,x1+border):
        if x==0:
            row+="0"
        elif (abs(x)%5==0):
            row+="|"
        else:
            row+=" "
    print(row)

    for y in range(y0-border,y1+border):
        row=str(y).rjust(5)+" "
        for x in range(x0-border,x1+border):
            row+=[SPACE, ELF][Elf(x,y) in elves]
        print(row)
    print()

def moveElf(elf,neighbours,turnOrder,print_level):
    for direction in turnOrder:
        if all(Elf(elf.x+delta[0], elf.y+delta[1]) not in neighbours for delta in direction.check):
            # no neighbours in this direction, move the elf!
            delta = direction.check[1]
            return Elf(elf.x+delta[0], elf.y+delta[1])
    if print_level>2:
        print(f"NOT SURE ABOUT THIS FROM INSTRUCTIONS: {elf} unable to move in _any_ direction due to neighbours: {neighbours}")
    return elf

def getNeighbours(elf,elves):
    #neighbours = [other for other in elves if elf.nextTo(other)]
    neighbours = []
    for dx,dy in ALL_DELTAS:
        other = Elf(elf.x+dx, elf.y+dy)
        if other in elves:
            neighbours.append(other)
    return neighbours

# an idea, maybe premature optisiation, could be confusing, ...this function taking majority of the ~1.5s per turn
# def getNeighboursAfter(elf_i,elves):
#     elf = elves[elf_i]
#     neighbours_after = []
#     for other_i in range(elf_i+1,len(elves)):
#         other = elves[other_i]
#         if other.nextTo(elf):
#             neighbours_after.append(other)
#     return neighbours_after

def makeThemDance(input_elves,turns_allowed,print_level=0):
    elves = set()
    elves.update(input_elves.copy())
    moveOrder = [NORTH, SOUTH, WEST, EAST]
    num_elves = len(elves)
    if print_level>1:
        printTheElves(elves)
    turn = 0
    someMoved = True
    if turns_allowed <=0:
        turns_allowed = math.inf
    while turn < turns_allowed and someMoved:
        turn_start_time=elapsedTimeMs()
        turnOrder = moveOrder[turn%4:]+moveOrder[:turn%4]
        if print_level > 0:
            print(f"{elapsedTimeMs()} TURN {turn} using turnOrder {[t.name for t in turnOrder]}")
        turn+=1
        # ideas ... "seen" "neighbours_after for efficiency"
        new_elves = set()
        neighbour_map = {}
        for elf in elves:
            #TODO: consider trying to speed this up - taking the majority of ~1.5s per turn and after 100 turns there were still around 2k elves trying to move
            neighbours = getNeighbours(elf,elves)
            if len(neighbours) > 0:
                neighbour_map[elf]=neighbours
            else:
                new_elves.add(elf) # i.e. stays where it is
        if print_level>1:
            print(f"elves not needing to move: {new_elves}")
        if print_level > 0: print(f"\t{elapsedTimeMs()-turn_start_time} TURN neighbours calculated. {len(neighbour_map)} will try to move")

        if (len(new_elves) == num_elves):
            print("RETURNING EARLY AS NO ELVES NEEDED TO MOVE")
            someMoved=False
        if someMoved:
            #set up moves
            moving_elves = {}
            for elf in neighbour_map:
                neighbours = neighbour_map[elf]
                new_elf = moveElf(elf,neighbours,turnOrder,print_level)
                if new_elf in moving_elves:
                    # == clash! neither will move
                    other = moving_elves.pop(new_elf)
                    new_elves.add(other)
                    new_elves.add(elf)
                    if print_level>1:
                        print(f"elves not moving due to clash {other} and {elf}")
                else:
                    moving_elves[new_elf]=elf
            if print_level > 0: print(f"\t{elapsedTimeMs()-turn_start_time} TURN movers calculated")
            # record the ones that moved
            for new_elf in moving_elves:
                if print_level>1:
                    print(f"elf {moving_elves[new_elf]} is moving to {new_elf}")
                new_elves.add(new_elf)
            if print_level > 0: print(f"\t{elapsedTimeMs()-turn_start_time} TURN movers moved")
        # and get ready for the next round...
        if len(new_elves) != num_elves:
            print(f"ERROR - an elf has escaped (or sneaked in...) actual {len(new_elves)} while expected {num_elves}")
        elves = new_elves
        if print_level>1:
            printTheElves(elves)
    return elves,turn

def getRectangle(elves):
    min_x = min(elf.x for elf in elves)
    min_y = min(elf.y for elf in elves)
    max_x = max(elf.x for elf in elves)
    max_y = max(elf.y for elf in elves)
    return [min_x,min_y,max_x,max_y]

def rectanguleSpaces(elves):
    rect = getRectangle(elves)
    min_x,min_y,max_x,max_y = rect
    total_area = (1 + max_y - min_y) * (1 + max_x - min_x)
    free_space = total_area - len(elves)
    return free_space,rect

final_elves,turns_taken = makeThemDance(elves,number_of_turns,print_level)
free_space,rectangle = rectanguleSpaces(final_elves)
print(f"{elapsedTimeMs()} after {turns_taken} turns taken (out of {number_of_turns} allowed) with {len(elves)} resulted in a rectangle {rectangle} with free space of {free_space}")
if print_level>1:
    for elf in sorted(final_elves,key=lambda e: e.x*1000 + e.y):
        print(elf)

#0:00:14.668938 after 10 with 2399 resulted in a rectangle [-3, -4, 73, 74] with free space of 3684
# correct but almost certainly too slow...
# changes elves and new_elves to a set in the main loop and boom :)
# 0:00:11.619416 after 862 turns taken (out of 0 allowed) with 2399 resulted in a rectangle [-15, -12, 118, 116] with free space of 14887
# print(elapsedTimeMs(),"starting part2")
# part 2 covered
