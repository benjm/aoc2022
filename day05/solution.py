import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")
def addCol(cols, line):
    ci = 1
    for i in range(0,len(line),4):
        col = cols.get(ci,"")
        cval = line[i:i+4]
        if cval[0] == "[":
            cols[ci] = col+cval[1]
        ci+=1
    return cols
ncol = 0
cols = {}
instr = []
input = True
for line in lines:
    if input and len(line) == 0:
        input = False
        print(cols)
    elif input:
        col = addCol(cols,line)
    else:
        ins,nChar,fromW,cFrom,toW,cTo = line.split()
        nChar = int(nChar)
        cFrom = int(cFrom)
        cTo = int(cTo)
        cSource = cols.get(cFrom,"")
        cDest = cSource[:nChar][::-1] + cols.get(cTo,"")
        cSource = cSource[nChar:]
        cols[cFrom] = cSource
        cols[cTo] = cDest
        print(line)
        print(cols)

o = ""
for k in sorted(cols):
    o+=cols[k][0]
print(o)
print("starting part2")
#line 33 remove the[::-1]
