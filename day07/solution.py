import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

# size of every dir
# sum of all with size "at most 100000"
# key [pa/th] : value [size] and sum nested?
# list of all paths
# $ cd /
# $ cd d
# $ cd ..
# $ ls
# dir d
# n f
def pathToKey(path):return "/"+"/".join(path)
path = []
sizes = {}
for line in lines:
    if line.startswith("$ cd "):
        p = line[5:]
        if p == "/":
            path = []
        elif p == "..":
            path = path[:-1]
        else:
            path+=p.split("/")
        pkey = pathToKey(path)
        sizes[pkey]=sizes.get(pkey,0)
    elif line.startswith("$ ls") or line.startswith("dir "):
        #print("ignored:",line,file=sys.stderr)
        pass
    else:
        sz,*fn=line.split()
        pkey = pathToKey(path)
        sizes[pkey]=sizes.get(pkey,0)+int(sz)
        for i in range(1,len(path)+1):
            l = len(path)-i
            subpath = path[:l]
            pkey = pathToKey(subpath)
            sizes[pkey]=sizes.get(pkey,0)+int(sz)

#print(sizes)
tot = 0
for k in sizes:
    if sizes[k] <= 100000:
        tot+=sizes[k]
        #print(k,sizes[k],tot)
print(tot)

print("starting part2")
disk = 70000000
need = 30000000
bestDir = "/"
minDelete = need - (disk - sizes[bestDir])
print("using :",sizes[bestDir])
print("delete:",minDelete)
for k in sizes:
    if sizes[bestDir]>=sizes[k]>=minDelete:
        bestDir=k
print(bestDir,sizes[bestDir])