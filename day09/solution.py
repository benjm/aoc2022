import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

deltas={
    "U":[0,1],
    "D":[0,-1],
    "R":[1,0],
    "L":[-1,0]
}
h=[0,0]
t=[0,0]
toId = lambda p:str(p[0])+","+str(p[1])
def follow(h,t):
    hx,hy=h
    tx,ty=t
    dx,dy=hx-tx,hy-ty
    if abs(dx)==abs(dy)==2:
        tx+=(dx//2)
        ty+=(dy//2)
    elif abs(dx)==2:
        tx+=(dx//2)
        ty+=dy
    elif abs(dy)==2:
        ty+=(dy//2)
        tx+=dx
    return [tx,ty]
been=set()
been.add(toId(t))
for line in lines:
    dirn,steps=line.split()
    for d in dirn*int(steps):
        dx,dy=deltas[d]
        x,y=h
        h=[x+dx,y+dy]
        t=follow(h,t)
        been.add(toId(t))
print(len(been))

def printRope(rope):
    print(rope)
    ys = [p[1] for p in rope]
    xs = [p[0] for p in rope]
    for y in range(max(ys)+5,min(ys)-1,-1):
        row=""
        for x in range(min(xs),max(xs)+5):
            if [x,y] in rope:
                i = rope.index([x,y])
                row+=([str(i),"H"][i==0])
            else:
                row+=(".")
        print(row)
    print()
    print()

print("starting part2")
rope = []
for i in range(10):
    rope.append([0,0])
been=set()
been.add(toId(rope[-1]))
for line in lines:
    dirn,steps=line.split()
    for d in dirn*int(steps):
        dx,dy=deltas[d]
        h=rope[0]
        rope[0] = [h[0]+dx,h[1]+dy]
        for i in range(len(rope)-1):
            rope[i+1]=follow(rope[i],rope[i+1])
        been.add(toId(rope[-1]))
    printRope(rope)
print(len(been))