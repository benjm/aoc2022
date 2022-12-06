import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1 - day04")

counter = 0
for line in lines:
    e1,e2=line.split(",")
    a1=a2=b1=b2=0
    if "-" in e1:
        a1,b1=map(int,e1.split("-"))
    else:
        a1=b1=int(e1)
    if "-" in e2:
        a2,b2=map(int,e2.split("-"))
    else:
        a2=b2=int(e2)
    if (a1<=a2 and b1>=b2) or (a2<=a1 and b2>=b1):
        counter+=1
print(counter)

print("starting part2")


counter = 0
for line in lines:
    e1,e2=line.split(",")
    a1=a2=b1=b2=0
    if "-" in e1:
        a1,b1=map(int,e1.split("-"))
    else:
        a1=b1=int(e1)
    if "-" in e2:
        a2,b2=map(int,e2.split("-"))
    else:
        a2=b2=int(e2)
    if a2<=a1<=b2 or a2<=b1<=b2 or a1<=a2<=b1 or a1<=b2<=b1:
        counter+=1
print(counter)