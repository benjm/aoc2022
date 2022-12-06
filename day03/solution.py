import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1 - day03")

az = "abcdefghijklmnopqrstuvwxyz"
priority = "_"+az+az.upper()
tot = 0
for line in lines:
    half = len(line)//2
    p1 = line[:half]
    p2 = line[half:]
    dbl = set()
    for c in p1:
        if c in p2:
            dbl.add(c)
    tot+=priority.index(dbl.pop())
print(tot)

print("starting part2")

tot = 0
for i in range(0,len(lines),3):
    r1,r2,r3=lines[i:i+3]
    common = set()
    for item in r1:
        if item in r2 and item in r3:
            common.add(item)
    tot+=priority.index(common.pop())
print(tot)