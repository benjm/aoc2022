import sys
import math
from dataclasses import dataclass
from datetime import datetime
import re

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

RIGHT,DOWN,LEFT,UP = FACING = [0,1,2,3]
FACING_S = [">","v","<","^"]
FACING_DELTA = [[1,0],[0,1],[-1,0],[0,-1]]
OPEN="."
SOLID="#"
SPACE=" "
CLOCKWISE="R"
ANTICLOCKWISE="L"
FLIP="F"
TURN="turn"
MOVE="move"

print_level=0
if len(sys.argv)>2:
    print_level=int(sys.argv[2])

@dataclass
class Position:
    x: int
    y: int
    facing: int
    panel_id: str
    def niceString(self):
        return f"Panel({self.panel_id} {FACING_S[self.facing]} @ {self.x}, {self.y})"

@dataclass
class Instruction:
    typ: str
    rot: str
    dist: int

@dataclass
class Row:
    offset: int
    tiles: str
    panel: str
    y: int

@dataclass
class Panel:
    id: str
    offset: int
    height: int
    width: int

# Cuboid wrapping ... hahaha ... gulp
# naughty plan - could do input specific wrapping?
# input cube is laid out roughly as below
#
#      i jg h
#     l111222d
#      111222     ".12" PROW0
#     k111222c
#     m333a b
#      333        ".3." PROW1
#   m n333b  
#  k444555c
#   444555        "45." PROW2
#  l444555d 
#  i666e f
#   666           "6.." PROW3
#  j666f
#   g h      
#
PROW0,PROW1,PROW2,PROW3 = HARDCODED_PANEL_ROWS = [".12", ".3.", "45.", "6.."]

PANEL_HEIGHT=PANEL_WIDTH=0

def processLines(lines):
    readingMap = True
    position = None
    layout = []
    instructions = []

    width=max(len(line) for line in lines[:-2])
    height=len(lines)-2

    panels={}
    x_panels=3
    y_panels=4 - (width==height)
    # if len(sys.argv)>4:
    #     x_panels=int(sys.argv[3])
    #     y_panels=int(sys.argv[4])
    panel_width = width//x_panels
    panel_height = height//y_panels

    for i in range(y_panels):
        panel_row_id = HARDCODED_PANEL_ROWS[i]
        offset = i*panel_height
        panels[panel_row_id]=Panel(panel_row_id,offset,panel_height,panel_width)

    for y in range(len(lines)):
        line=lines[y]
        if readingMap:
            if len(line)==0:
                readingMap=False
            else:
                end = len(line)
                data = line.lstrip()
                offset = end - len(data)
                pri=0
                panel_id=HARDCODED_PANEL_ROWS[y//panel_height]
                row=Row(offset,data,panel_id, y)
                print(row)
                layout.append(row)
                if not position:
                    position = Position(offset,y,RIGHT,panel_id)
        else:
            for raw_ins in re.findall('\d+|\D+', line):
                if raw_ins in [CLOCKWISE, ANTICLOCKWISE]:
                    instructions.append(Instruction(TURN,raw_ins,None))
                else:
                    instructions.append(Instruction(MOVE,None,int(raw_ins)))
    return layout,instructions,position,width,height,panels

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

def printMap(layout,position):
    print()
    for i in range(len(layout)):
        row=layout[i]
        full_row = row.offset*SPACE+row.tiles
        if i==position.y:
            full_row =full_row[:position.x]+FACING_S[position.facing]+full_row[position.x+1:]
        print(full_row)
    print()

def turn(position,rot,print_level):
    facing = position.facing
    max_facing=len(FACING)-1
    if rot==CLOCKWISE:
        facing=[0, facing+1][facing<max_facing]
    elif rot==ANTICLOCKWISE:
        facing=[max_facing, facing-1][facing>0]
    elif rot==FLIP:
        facing = [facing-2, facing+2][facing < (max_facing-1)]
    else:
        print(f"ERROR applying rotation '{rot}' to  {position}")
    if print_level>1:
        print(f"Rotate {rot} changes {position.facing} to {facing}")
    position.facing=facing
    return position

def getWrapToPosition(from_panel_id,from_position,print_level):
    # Awful convoluted if...elif...etc statement.
    # TODO: Refactor into panels/sides of a cube with behaviours.
    # Sides of cube could retain global co-ord reference for the final password calc.
    x = from_position.x
    y = from_position.y
    facing = from_position.facing
    if from_panel_id != from_position.panel_id:
        print(f"ERROR from_panel_id={from_panel_id} but position data is {from_position.niceString()}")

    from_panel = panels[from_panel_id]
    panel_width = from_panel.width
    panel_height = from_panel.height

    to_panel_id = new_facing = new_x = new_y = None
    # (zero index inversion with height ... was height the full height so ... is this going to be an off by one annoyance?)

    if from_panel_id == PROW0:
        if facing == LEFT:
            to_panel_id = PROW2 
            new_facing = RIGHT
            new_x = 0
            y_delta = panel_height - y - 1 
            new_y = panel_height*2 + y_delta

        elif facing == RIGHT:
            to_panel_id = PROW2 
            new_facing = LEFT
            new_x = panel_width * 2 - 1
            y_delta = panel_height - y - 1 
            new_y = panel_height * 2 + y_delta

        elif facing == DOWN:
            to_panel_id = PROW1
            new_facing = LEFT
            new_x = panel_width * 2 - 1
            y_delta = x - 2 * panel_width
            new_y = panel_height + y_delta

        elif facing == UP:
            to_panel_id = PROW3
            # due to the folds this is the only place where a direction out a panel row has two destination panels
            if from_position.x >= panel_width*2:
                new_facing = UP
                new_y = panel_height * 4 - 1 # == height - 1
                new_x = x - 2 * panel_width
            else:
                new_facing = RIGHT
                new_x = 0
                new_y = 3 * panel_height + (x - panel_width)

    elif from_panel_id == PROW1:
        if facing == LEFT:
            to_panel_id = PROW2
            new_facing = DOWN
            new_y = 2 * panel_height
            new_x = y - panel_height

        elif facing == RIGHT:
            to_panel_id = PROW0
            new_facing = UP
            new_y = panel_height - 1
            new_x = (y - panel_height) + 2 * panel_width

    elif from_panel_id == PROW2:
        if facing == LEFT:
            to_panel_id = PROW0 
            new_facing = RIGHT
            new_x = panel_width
            new_y = (panel_height - (y - 2 * panel_height))-1

        elif facing == RIGHT:
            to_panel_id = PROW0 
            new_facing = LEFT
            new_x = 3 * panel_width - 1
            new_y = (panel_height - (y - 2 * panel_height))-1

        elif facing == DOWN:
            to_panel_id = PROW3
            new_facing = LEFT
            new_x = panel_width - 1
            new_y = (x - panel_width) + 3 * panel_height

        elif facing == UP:
            to_panel_id = PROW1
            new_facing = RIGHT
            new_x = panel_width
            new_y = x + panel_height

    elif from_panel_id == PROW3:
        if facing == LEFT:
            to_panel_id = PROW0 # y inverted flipped
            new_facing = DOWN
            new_y = 0
            new_x = (y - 3 * panel_height) + panel_width

        elif facing == RIGHT:
            to_panel_id = PROW2 # y inverted flipped
            new_facing = UP
            new_y = panel_height * 3 - 1
            new_x = (y - 3 * panel_height) + panel_width

        elif facing == DOWN:
            to_panel_id = PROW0
            new_facing = DOWN
            new_y = 0
            new_x = x + panel_width * 2
                             
    new_position = Position(new_x, new_y, new_facing, to_panel_id)
    print(f"WRAP from {from_position.niceString()} round to {new_position.niceString()} (NB panel w,h={panel_width},{panel_height})")
    return new_position

# Cuboid wrapping ... hahaha ... gulp
# naughty plan - input (known) specific wrapping
# input cube is laid out as below with links as shown
#
#      i jg h
#     l111222d
#      111222     ".12" PROW0
#     k111222c
#     m333a b
#      333        ".3." PROW1
#   m n333b  
#  k444555c
#   444555        "45." PROW2
#  l444555d 
#  i666e f
#   666           "6.." PROW3
#  j666f
#   g h      
#  
# error in wrapping?
# 0:00:00.016875 password from Position(x=21, y=110, facing=1, panel_id='45.') calculated to be 111089 is too high
# 0:00:00.016921 password from Position(x=62, y=75, facing=3, panel_id='.3.') calculated to be   76255 is too low
# manually checked logic based on logging output (more than one of every cube face transition in that) and fixed one error in the middle of that horrible if statement mess
# 0:00:00.015967 password from Position(x=72, y=99, facing=3, panel_id='45.') calculated to be 100295 is too low
# re-added the to_move decrement in the wrapMove function ... at the correct indentation (doh)
# 0:00:00.016045 password from Position(x=95, y=103, facing=1, panel_id='.3.') calculated to be 104385 CORRECT!

def wrapMove(position,layout,to_move,column_limits,print_level,cube_wrap):
    from_panel_id=layout[position.y].panel
    position.panel_id = from_panel_id

    new_position = getWrapToPosition(from_panel_id,position,print_level)
    # check ingress point on edge first & if unable to enter return position
    row = layout[new_position.y]
    if row.tiles[new_position.x - row.offset] == SOLID:
        return move(position,layout,0,column_limits,print_level,cube_wrap) # i.e. DON'T move
    to_move-=1
    return move(new_position,layout,to_move,column_limits,print_level,cube_wrap)

    # while testing the wrapping info - loop back into move where you left off, only without the cube wrapping
    #return move(position,layout,to_move,column_limits,print_level,cube_wrap=False)

def move(position,layout,distance,column_limits,print_level,cube_wrap):
    if distance<1:
        return position
    dx,dy=FACING_DELTA[position.facing]
    to_move=distance
    if dy == 0:
        row=layout[position.y]
        x=position.x - row.offset
        max_x=len(row.tiles)-1
        while to_move>0:
            next_x = x+dx
            if next_x<0:
                if cube_wrap:
                    return wrapMove(position,layout,to_move,column_limits,print_level,cube_wrap)
                next_x=max_x
            elif next_x>max_x:
                if cube_wrap:
                    return wrapMove(position,layout,to_move,column_limits,print_level,cube_wrap)
                next_x=0
            if row.tiles[next_x]==SOLID:
                to_move=0
            else:
                x=next_x
                position.x=x+row.offset
                to_move-=1
    elif dx==0:
        y=position.y
        min_y,max_y=column_limits[position.x]
        while to_move>0:
            next_y = y+dy
            if next_y>max_y:
                if cube_wrap:
                    return wrapMove(position,layout,to_move,column_limits,print_level,cube_wrap)
                next_y=min_y
            elif next_y<min_y:
                if cube_wrap:
                    return wrapMove(position,layout,to_move,column_limits,print_level,cube_wrap)
                next_y=max_y
            row = layout[next_y]
            x=position.x-row.offset
            if row.tiles[x]==SOLID:
                to_move=0
            else:
                y=next_y
                position.y=y
                to_move-=1
    else:
        print(f"ERROR moving {distance} from {position}")
    return position

def findFirstY(layout,x):
    for y in range(height):
        row=layout[y]
        if x>=row.offset and x<row.offset+len(row.tiles):
            return y
    print("ERROR findFirstY for x =",x)
    return height

def findLastY(layout,x):
    for y in range(height-1,-1,-1):
        row=layout[y]
        if x>=row.offset and x<row.offset+len(row.tiles):
            return y
    print("ERROR findLastY for x =",x)
    return -1

def getColumnLimits(layout,width):
    # TODO maybe do this during the initial processing phase - create a transposed layout
    column_limits={}
    for x in range(width):
        min_y = findFirstY(layout,x)
        max_y = findLastY(layout,x)
        min_max=[min_y,max_y]
        column_limits[x]=min_max
    return column_limits

def followInstructions(layout,position,column_limits,instructions,print_level=0,cube_wrap=False):
    if cube_wrap:
        print("USING CUBE WRAPPING DATA")
    for instruction in instructions:
        if instruction.typ == TURN:
            position=turn(position,instruction.rot,print_level)
        elif instruction.typ == MOVE:
            position=move(position,layout,instruction.dist,column_limits,print_level,cube_wrap)
        if print_level>1:
            print(instruction)
            printMap(layout,position)
    return position

def calculatePassword(position):
    return 1000 * (position.y+1) + 4 * (position.x+1) + position.facing

print(elapsedTimeMs(),"starting part1 - day21")

layout,instructions,position,width,height,panels = readFile()
print("first few instructions:",instructions[:10])

column_limits = getColumnLimits(layout,width)
print(elapsedTimeMs(),"column limits calculated")

if print_level>0:
    printMap(layout,position)

final_position=followInstructions(layout,position,column_limits,instructions,print_level)
password=calculatePassword(final_position)
print(f"{elapsedTimeMs()} password from {final_position} calculated to be {password}")
# hmmm ... test fine at 6032 but input value of 5491 was too low
# error found in turn function where failed to rotate from ^ to > ... oops :)
# real ans for part 1 was 0:00:00.006669 password from Position(x=86, y=56, facing=2) calculated to be 57350

print(elapsedTimeMs(),"starting part2 - day21")

## RESET
layout,instructions,position,width,height,panels = readFile()
final_position=followInstructions(layout,position,column_limits,instructions,print_level,cube_wrap=True)
password=calculatePassword(final_position)
print(f"{elapsedTimeMs()} password from {final_position} calculated to be {password}")

