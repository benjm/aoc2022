import sys
import math
from dataclasses import dataclass
from datetime import datetime

filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

datetime_start = datetime.now()
def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

@dataclass
class Valve:
    id: str
    rate: int
    links: list

valves=[]
valveMap={}
for line in lines:
    l,r=line.split(";")
    ll,lr=l.split("=")
    rate=int(lr)
    id = ll.split()[1]
    rs = r.split(", ")
    links=[rs[0].split()[-1]]
    if len(rs)>1:
        links+=rs[1:]
    valve=Valve(id,rate,links)
    valves.append(valve)
    valveMap[valve.id]=valve

#OM(F)G ... you start from AA whether the *^%$"£ input starts with AA or not" ... took hours and a hint for this little gem of information to surface
valves=sorted(valves, key=lambda v: v.id)

distances = {} #(valve id tuple) : min_distance
def calcDistances(a,others):
    others = [v for v in others if (a.id,v.id) not in distances and a.id != v.id]
    been = set()
    been.add(a.id)
    ends = set()
    ends.add(a.id)
    dist = 0
    while len(ends) > 0 and any(v.id not in been for v in others):
        dist+=1
        new_ends=set()
        for end in ends:
            valve=valveMap[end]
            new_ends.update(vid for vid in valve.links if vid not in been)
        been.update(new_ends)
        for end in new_ends:
            distances[(end,a.id)]=dist
            distances[(a.id,end)]=dist
        ends = new_ends

def getShortestPath(a_id, b_id):
    a = valveMap[a_id]
    paths=[]
    been=set()
    been.add(a.id)
    paths.append([a.id])
    while b_id not in been:
        new_paths=[]
        for path in paths:
            end_id = path[-1]
            links = [link for link in valveMap[end_id].links if link not in been]
            been.update(links)
            for link in links:
                if link == b_id:
                    return path+[link] # END EARLY
                new_paths.append(path.copy()+[link])
        paths = new_paths
    return [a.id]

useful_valves=[v for v in valves if v.rate>0]
useful_valve_ids=[v.id for v in useful_valves]
print(f"there are {len(valves)} valves in total")
print(f"there are {len(useful_valves)} valves with a non-zero flow rate: {[v.id for v in useful_valves]}")
print("Useful Valves",useful_valve_ids)

calcDistances(valves[0],useful_valves)
for i in range(len(useful_valves)):
    valve = useful_valves[i]
    others = useful_valves[:i]+useful_valves[i+1:]
    calcDistances(valve, others)

# useful_distances = {}
# for pair in distances:
#     a,b = pair
#     if a in useful_valve_ids and b in useful_valve_ids:
#         useful_distances[pair] = distances[pair]
# print(f"Recorded {len(useful_distances)} useful distances (NB both 'a to b' and 'b to a' should be in there)")

print()
print(elapsedTimeMs(),"starting part1")

@dataclass
class Path:
    pos_id: str
    prev_id: str
    time_left: int
    pressure: int
    total_pressure: int
    been_ids: list

start_path = Path(valves[0].id, None, 30, 0, 0, [valves[0].id])
paths = [start_path]
best_path = start_path

n=0
while len(paths)>0:
    n+=1
    if n%1==0:
        print(f"Iteration {n} will follow {len(paths)} paths. {best_path.total_pressure}")
    new_paths=[]
    for path in paths:
        valve = valveMap[path.pos_id]
        target_ids = [vid for vid in useful_valve_ids if vid not in path.been_ids]
        
        if len(target_ids) == 0 and path.total_pressure > best_path.total_pressure:
            best_path = path

        for target_id in target_ids:
            dist = distances[(valve.id, target_id)]
            time_needed = dist+1
            if time_needed < path.time_left:
                target = valveMap[target_id]
                time_left = path.time_left - time_needed
                total_pressure = path.total_pressure + target.rate * time_left
                new_pressure = path.pressure + target.rate
                been = path.been_ids.copy()
                been.append(target.id)
                new_path = Path(target.id, path.pos_id, time_left, new_pressure, total_pressure, been)
                new_paths.append(new_path)
            elif path.total_pressure > best_path.total_pressure:
                best_path = path
            #else discard branch
    paths = new_paths

print(elapsedTimeMs(),"BEST PATH JUST ME",best_path.total_pressure)

print("Best Path in detail:")
t=0
pressure_per_minute=0
total_pressure=0
pos = valves[0]
print("T\tID\tP\tPPM\tTOT")
print(f"{t+1}\t{pos.id}\t0\t{pressure_per_minute}\t{total_pressure}\tmove")
for target in [valveMap[v_id] for v_id in best_path.been_ids[1:]]:
    gapt=t
    dist = distances[(pos.id, target.id)]
    t+=dist+1
    for stop_id in getShortestPath(pos.id, target.id)[1:]:
        gapt+=1
        action=["move","open valve"][gapt+1 == t]
        print(f"{gapt+1}\t{stop_id}\t~\t{pressure_per_minute}\t{total_pressure}\t{action}")
    pressure_per_minute+=target.rate
    pos=target
    time_left = 30-t
    over_time=target.rate * time_left
    total_pressure+=over_time
    print(f"{t+1}\t{pos.id}\t{target.rate}\t{pressure_per_minute}\t{total_pressure}\tmove")
if t<30:
    print("no futher moves or opening of valves")
print()

# # PART 1 first attempt
#     # first attempt is waaaaay too poorly optimised and would take around 70 days to complete X-D
#     # testing path 10,000,000 of 1,307,674,368,000 paths 0:00:46.253643
#     import itertools
#     max_total_flow=0
#     best_path=[]
#     num_paths = math.factorial(len(useful_valves))
#     print(f"testing {num_paths} paths...")
#     pi=0
#     for path in itertools.permutations(useful_valves):
#         pi+=1
#         if pi%1000000==0:
#             print(f"testing path {pi} of {num_paths} paths {elapsedTimeMs()}")
#         t=0
#         pressure_per_minute=0
#         total_pressure=0
#         pos = valves[0]
#         for target in path:
#             pressure_per_minute+=target.rate
#             dist = distances[(pos.id, target.id)]
#             t+=dist+1
#             pos=target
#             time_left = 30-t
#             if time_left>0:
#                 over_time=target.rate * time_left
#                 total_pressure+=over_time
#         if total_pressure > max_total_flow:
#             max_total_flow = total_pressure
#             best_path = path
#     print("Best Route:")
#     t=0
#     pressure_per_minute=0
#     total_pressure=0
#     pos = valves[0]
#     print(t,pos.id,pressure_per_minute,total_pressure)
#     for target in best_path:
#         pressure_per_minute+=target.rate
#         dist = distances[(pos.id, target.id)]
#         t+=dist+1
#         pos=target
#         time_left = 30-t
#         over_time=target.rate * time_left
#         total_pressure+=over_time
#         print(t,pos.id,pressure_per_minute,over_time,total_pressure)

#     print("Total Flow:",total_pressure)
#     print()

print()
print(elapsedTimeMs(),"starting part2")
# 26 minutes
# two paths active at once...

### PART 1 REPEATED FOR INSPIRATION...
# @dataclass
# class Path:
#     pos_id: str
#     prev_id: str
#     time_left: int
#     pressure: int
#     total_pressure: int
#     been_ids: list

def updatePath(path, target_id):
    if path.pos_id == target_id: # this one is not changing
        return path
    dist = distances[(path.pos_id, target_id)]
    time_needed = dist+1
    if time_needed >= path.time_left:
        return finishPath(path)
    target = valveMap[target_id]
    time_left = path.time_left - time_needed
    total_pressure = path.total_pressure + target.rate * time_left
    new_pressure = path.pressure + target.rate
    been = path.been_ids.copy()
    been.append(target.id)
    return Path(target.id, path.pos_id, time_left, new_pressure, total_pressure, been)

def finishPath(path):
    return Path(path.pos_id,path.prev_id,0,path.pressure,path.total_pressure,path.been_ids.copy())

def updatePair(path_a,path_b,target_a,target_b):
    global best_pair # not required for the test scenario but crashes with errors in the input scneario due to assignment making it a local variable somehow
    new_path_pair = (updatePath(path_a,target_a), updatePath(path_b, target_b))
    if all(p.time_left <= 0 for p in new_path_pair):
        new_path_pressure = sum(p.total_pressure for p in new_path_pair)
        best_path_pressure = sum(p.total_pressure for p in best_pair)
        if new_path_pressure > best_path_pressure:
            best_pair = new_path_pair
        return None
    else:
        return new_path_pair

def cullPaths(path_pairs,starting_best,cull_bottom):
    min_required = int(cull_bottom * starting_best)
    return [pair for pair in path_pairs if sum(p.total_pressure for p in pair) > min_required]

start_path_1 = Path(valves[0].id, None, 26, 0, 0, [valves[0].id])
start_path_2 = Path(valves[0].id, None, 26, 0, 0, [valves[0].id])

best_pair = (start_path_1,start_path_2)
path_pairs = [(start_path_1,start_path_2)]
n=0
import itertools
while len(path_pairs)>0:
    n+=1
    starting_best=sum(p.total_pressure for p in best_pair)
    starting_pairs=len(path_pairs)
    print(f"{elapsedTimeMs()} Iteration {n} will follow {starting_pairs} path_pairs. {starting_best}")
    if n>=6:
        cull_bottom = 0.8
        path_pairs = cullPaths(path_pairs,starting_best,cull_bottom)
        print(f"{elapsedTimeMs()} Iteration {n} culling bottom {cull_bottom} reduced pairs to check to {len(path_pairs)}")
    m=0
    new_path_pairs=[]
    for (path_a,path_b) in path_pairs:
        m+=1
        if m%1000000==0:
            print(f"{elapsedTimeMs()} Iteration {n} is up to path_pair {m}")
        combined_been_ids = set()
        combined_been_ids.update(path_a.been_ids)
        combined_been_ids.update(path_b.been_ids)
        target_ids = [vid for vid in useful_valve_ids if vid not in combined_been_ids]
        # do we need to test for state where no more target ids exits?
        if len(target_ids) == 0:
            new_path_pair = (finishPath(path_a),finishPath(path_b))
            new_path_pressure = sum(p.total_pressure for p in new_path_pair)
            best_path_pressure = sum(p.total_pressure for p in best_pair)
            if new_path_pressure > best_path_pressure:
                best_pair = new_path_pair
        elif path_a.time_left == path_b.time_left:
            #if only one to pick from - two branches to test
            if len(target_ids)==1:
                for target_a,target_b in [(target_ids[0], path_b.pos_id),(path_a.pos_id, target_ids[0])]:
                    new_path_pair = updatePair(path_a,path_b,target_a,target_b)
                    if new_path_pair:
                        new_path_pairs.append(new_path_pair)
            else: # get all possible iterations
                for target_a,target_b in itertools.permutations(target_ids, 2):
                    new_path_pair = updatePair(path_a,path_b,target_a,target_b)
                    if new_path_pair:
                        new_path_pairs.append(new_path_pair)
        elif path_a.time_left > path_b.time_left: # update A
            target_b = path_b.pos_id
            for target_a in target_ids:
                new_path_pair = updatePair(path_a,path_b,target_a,target_b)
                if new_path_pair:
                    new_path_pairs.append(new_path_pair)
        else: # update B
            target_a = path_a.pos_id
            for target_b in target_ids:
                new_path_pair = updatePair(path_a,path_b,target_a,target_b)
                if new_path_pair:
                    new_path_pairs.append(new_path_pair)
    path_pairs = new_path_pairs
print(elapsedTimeMs(),"BEST PATH plus an ELEPHANT and ME",sum(p.total_pressure for p in best_pair))

# with a cull of 0.5 python ram usage hit 38Gb ... and iteration 7 up to 64M pairs after 42 minutes!

# with a cull of 0.8 the solution was found (!!)
# 0:00:00.858663 starting part2
# 0:00:00.858674 Iteration 1 will follow 1 path_pairs. 0
# 0:00:00.859096 Iteration 2 will follow 210 path_pairs. 0
# 0:00:00.875371 Iteration 3 will follow 7306 path_pairs. 0
# 0:00:01.347604 Iteration 4 will follow 150920 path_pairs. 1109
# 0:00:09.408808 Iteration 5 will follow 2173324 path_pairs. 1576
# 0:00:43.683891 Iteration 5 is up to path_pair 1000000
# 0:01:22.714106 Iteration 5 is up to path_pair 2000000
# 0:01:27.138830 Iteration 6 will follow 19262680 path_pairs. 1969
# 0:01:34.434651 Iteration 6 culling bottom 0.8 reduced pairs to check to 238808
# 0:01:42.668724 Iteration 7 will follow 1381026 path_pairs. 2065
# 0:01:43.036511 Iteration 7 culling bottom 0.8 reduced pairs to check to 717812
# 0:02:02.048749 Iteration 8 will follow 2170428 path_pairs. 2218
# 0:02:02.643925 Iteration 8 culling bottom 0.8 reduced pairs to check to 613216
# 0:02:12.528343 Iteration 9 will follow 1116368 path_pairs. 2282
# 0:02:12.865535 Iteration 9 culling bottom 0.8 reduced pairs to check to 650914
# 0:02:23.292173 Iteration 10 will follow 640868 path_pairs. 2322
# 0:02:23.502486 Iteration 10 culling bottom 0.8 reduced pairs to check to 472524
# 0:02:28.809883 Iteration 11 will follow 235062 path_pairs. 2343
# 0:02:28.891223 Iteration 11 culling bottom 0.8 reduced pairs to check to 208344
# 0:02:30.599552 Iteration 12 will follow 38848 path_pairs. 2343
# 0:02:30.614256 Iteration 12 culling bottom 0.8 reduced pairs to check to 38848
# 0:02:30.919630 Iteration 13 will follow 1374 path_pairs. 2343
# 0:02:30.920300 Iteration 13 culling bottom 0.8 reduced pairs to check to 1374
# 0:02:30.933997 BEST PATH plus an ELEPHANT and ME 2343






