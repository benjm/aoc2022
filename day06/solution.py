import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

for pkt in lines:
    found = False
    i = 0
    while (not found) and (i < len(pkt)-4):
        if len(set(pkt[i:i+4])) == 4:
            print(i+4)
            found = True
        i+=1

print("starting part2")

for pkt in lines:
    found = False
    i = 0
    while (not found) and (i < len(pkt)-14):
        if len(set(pkt[i:i+14])) == 14:
            print(i+14)
            found = True
        i+=1