import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

noop = "noop"
addx = "addx"
x=1
c=1
hist=[x]
for ins in lines:
    hist.append(x)
    if ins.startswith(noop):
        c+=1
    elif ins.startswith(addx):
        x+=int(ins.split()[1])
        hist.append(x)
        c+=2
totstrength=0
for i in range(19,220,40):
    h=hist[-1]
    if i < len(hist):
        h=hist[i]
    strength = h*(i+1)
    totstrength+=strength
    #print("turn",i)
    #print(hist[i-1:i+2],h,strength,totstrength)
print(totstrength)

print("starting part2")
sprite_width=3
width=40
height=6
for y in range(height):
    row=""
    for x in range(width):
        crt_i = y*width+x
        d = abs(hist[crt_i]-x)
        row+=["#"," "][d>1]
    print(row)