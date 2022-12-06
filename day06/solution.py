import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

def unique(pkt,sze):
    i = 0
    while i < len(pkt)-sze:
        if len(set(pkt[i:i+sze])) == sze:
            return i+sze
        i+=1
    return(-1)

for pkt in lines:
    print(unique(pkt,4))

print("starting part2")

for pkt in lines:
    print(unique(pkt,14))
