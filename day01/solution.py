import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

elves = []
running_total = 0
for line in lines:
    if not line and running_total>0:
        elves.append(running_total)
        running_total=0
    else:
        running_total+=int(line)
if running_total>0:
    elves.append(running_total)

print(max(elves))

print("starting part2")

print(sum(sorted(elves)[-3:]))