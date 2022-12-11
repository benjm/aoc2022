import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()


sep=","
toId=lambda x,y:str(x)+sep+str(y)
fromId=lambda id:map(int,id.split(sep))

height = len(lines)
width = len(lines[0])
forest = []
for line in lines:
    print(line)
    forest.append([*map(int,line)])

# forest_transposed = []
# for y in range(width):
#     forest_transposed.append([])
#     for x in range(height):
#         forest_transposed[y].append(-1)

# for y in range(height):
#     for x in range(width):
#         forest_transposed[x][y] = forest[y][x]

print("starting part1")
vis=set()

# edges
vis.update(map(toId,range(width),[0]*width))
vis.update(map(toId,range(width),[height-1]*width))
vis.update(map(toId,[0]*height,range(height)))
vis.update(map(toId,[width-1]*height,range(height)))

def scan_heights(frow):
    vis = set()

for y in range(1,height-1):
    top=-1
    x_indeces = set()
    for x in range(width):
        t = forest[y][x]
        if t>top:
            top=t
            x_indeces.add(x)
    top = -1
    for x in range(width-1,-1,-1):
        t = forest[y][x]
        if t>top:
            top=t
            x_indeces.add(x)
    vis.update(map(toId,x_indeces,[y]*len(x_indeces)))

for x in range(1,width-1):
    top = -1
    y_indeces = set()
    for y in range(height):
        t=forest[y][x]
        if t>top:
            top=t
            y_indeces.add(y)
    top=-1
    for y in range(height-1,-1,-1):
        t=forest[y][x]
        if t>top:
            top=t
            y_indeces.add(y)
    vis.update(map(toId,[x]*len(y_indeces),y_indeces))

for y in range(height):
    row=""
    for x in range(width):
        row+=[".","T"][toId(x,y) in vis]
    print(row)

print("xy visible",len(vis))


print("starting part2")
def look(x,y,dx,dy,forest):
    h = len(forest)
    w = len(forest[0])
    t = forest[y][x]
    n = -1
    see=0
    while n<t:
        y+=dy
        x+=dx
        if (w>x>=0) and (h>y>=0):
            see+=1
            n=forest[y][x]
        else:
            n=t
    return see

highest_schenic_score = 0
tx=ty=-1
for y in range(1,height-1):
    for x in range(1,width-1):
        views = [look(x,y,0,1,forest) , look(x,y,0,-1,forest) , look(x,y,1,0,forest) , look(x,y,-1,0,forest)]
        scenic_score = math.prod(views)
        #print("views from "+toId(x,y)+ "[dn,up,ri,le]",views,scenic_score)
        if scenic_score>highest_schenic_score:
            highest_schenic_score = scenic_score
print(highest_schenic_score)