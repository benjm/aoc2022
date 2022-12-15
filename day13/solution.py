import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

class MyClass:
    def __init__(self, id):
        self.id=id
    def __str__(self):
        return f"MyClass {self.id}"

print("starting part1")

def splitEntry(s):
    o=[]
    b=0
    if s.startswith("["):
        s=s[1:-1]
    v=""
    for c in s:
        if b==0 and c==",":
            o.append(v)
            v=""
        else:
            if c=="[":
                b+=1
            elif c=="]":
                b-=1
            v+=c
    if len(v)>0:
        o.append(v)
    return o

right,wrong,ignore="right wrong ignore".split()
def checkOrder(l,r):
    if l.startswith("[") and r.startswith("["):
        l=splitEntry(l)
        r=splitEntry(r)
        #print(f"checking lists {l} and {r}")
        for i in range(min(len(l),len(r))):
            result = checkOrder(l[i],r[i])
            if result == wrong:
                return wrong
            elif result == right:
                return right
        if len(l) > len(r):
            #print("r ran out first")
            return wrong
        elif len(l) < len(r):
            #print("l ran out first")
            return right
        #print("no decision based on",l,"and",r)
        return ignore
    elif l.startswith("["):
        #print("just l is a list")
        return checkOrder(l,"["+r+"]")
    elif r.startswith("["):
        #print("just r is a list")
        return checkOrder("["+l+"]",r)
    else:
        #print(f"checking {l} <= {r}")
        return [[ignore, wrong][int(l) > int(r)],right][int(l) < int(r)]
    print("DUNNO HOW YOU GOT TO HERE!")
    return ignore

tot=0
n=0
x=0
d1="[[2]]"
d2="[[6]]"
pairs=[d1,d2]
for i in range(0,len(lines),3):
    x+=2
    pairIndex = 1 + (i+1)//3
    # print("PAIR",pairIndex,"...checking...")
    # print(lines[i])
    # print(lines[i+1])
    pairs.append(lines[i])
    pairs.append(lines[i+1])
    result = checkOrder(lines[i],lines[i+1])
    # print("PAIR",pairIndex,["NOT","IS"][result in [right,ignore]],"in the right order")
    # print()
    if result in [right,ignore]:
        tot+=pairIndex
        n+=1

print(n,"pairs in right order out of",x,", giving total of right order pair indeces:",tot)

print("starting part2")

def sorter(l,r):
    return {right:-1,wrong:1,ignore:0}[checkOrder(l,r)]

import functools
pairs = sorted(pairs,key=functools.cmp_to_key(sorter))
# for pair in pairs:
#     print(pair)

i1=pairs.index(d1)+1
i2=pairs.index(d2)+1
print(i1,"x",i2,"=",i1*i2)
