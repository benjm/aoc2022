import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()
def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

# class MyClass:
#     def __init__(self, id):
#         self.id=id
#     def __str__(self):
#         return f"MyClass {self.id}"

@dataclass
class Robot:
    typ: str
    resources: list

ORE="ore"
CLAY="clay"
OBSIDIAN="obsidian"
GEODE="geode"
TYPES=[ORE,CLAY,OBSIDIAN,GEODE]

def readBlueprints(lines,prnt=True):
    blueprints={}
    for blueprint in lines:
        #Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
        blueprint_id,robot_costs=blueprint.split(": ")
        blueprint_id = int(blueprint_id.split()[1])
        if prnt:
            print("Blueprint id:",blueprint_id)
        robot_data=[]
        robot_map={}
        for robot_cost in robot_costs.split(". "):
            each_robot_txt, ore_cost = robot_cost.split(" costs ")
            robot_typ = each_robot_txt.split()[1]
            cost={}
            for entry in ore_cost.replace(".","").split(" and "):
                ore_req_s, ore_typ=entry.split()
                cost[ore_typ]=int(ore_req_s)
            robot=Robot(robot_typ, [cost.get(ORE,0), cost.get(CLAY,0), cost.get(OBSIDIAN,0), 0])
            robot_data.append(robot)
            robot_map[robot_typ]=robot
            if prnt:
                print(f"\t{robot}")
        blueprints[blueprint_id]=robot_map
    if prnt:
        print(elapsedTimeMs(),"READ BLUEPRINTS")
    return blueprints

blueprints=readBlueprints(lines,prnt=True)

print(elapsedTimeMs(),"starting part1")

@dataclass
class BuildOrder:
    time_left: int
    resources: list
    robots: list
    built: list
    def new(t):
        return BuildOrder(t,[0,0,0,0],[1,0,0,0],[])
    def copy(self):
        return BuildOrder(self.time_left,self.resources.copy(),self.robots.copy(),self.built.copy())
    def current_max_geodes(self):
        return self.resources[3] + self.robots[3] * self.time_left

def checkCanBuild(robot, path):
    min_required = 0
    for i in range(3):
        if robot.resources[i] > 0:
            if path.robots[i] < 1:
                return False,None
            ore_to_collect=robot.resources[i] - path.resources[i] # any negative value will be ignored
            time_to_collect = math.ceil(ore_to_collect / path.robots[i])
            min_required=max(min_required, time_to_collect)
    min_required+=1 # takes one minute to build after gathering the resources
    time_left = path.time_left - min_required
    if time_left<=0:
        return False,None
    resources = []
    for i in range(4):
        resources.append(path.resources[i] + path.robots[i] * min_required - robot.resources[i])
    robots = path.robots.copy()
    robots[TYPES.index(robot.typ)]+=1
    built = path.built.copy()
    built.append(robot.typ)
    new_path = BuildOrder(time_left, resources, robots, built)
    return True, new_path

def canCompete(path,best_path,max_time):
    if path.time_left > 10 or (best_path.current_max_geodes() <= path.current_max_geodes() + path.time_left):
        return True
    if path.current_max_geodes() + path.time_left * (path.robots[3]+2) < best_path.current_max_geodes():
        return False
    return True # default

def findMaxGeodes(robot_map, minutes_allowed):
    max_useful_robots=[max(r.resources[i] for r in robot_map.values()) for i in range(4)]
    #time_left,resources[],robots[]
    max_geodes = 0
    # ref: TYPES=[ORE,CLAY,OBSIDIAN,GEODE]
    best_path=BuildOrder.new(minutes_allowed)
    print("starting best path:",best_path)
    paths=[best_path.copy()]
    max_track=0,0,0
    while len(paths)>0:
        new_paths=[]
        max_time=max(p.time_left for p in paths)
        l_before = len(paths)
        print(f"{elapsedTimeMs()} Starting next iteration... {l_before} paths with max time {max_time} (filtering skipped) with best so far of {max_geodes} geodes")
        # paths = [path for path in paths if canCompete(path, best_path,max_time)]
        # l_after = len(paths)
        # print(f"{elapsedTimeMs()} Starting next iteration... {l_before} paths with max time {max_time} filtered down to {l_after} with best so far of {max_geodes} geodes")
        m=0
        fo=0
        for path in paths:
            m+=1
            if m%1000000==0:
                print(f"\t{elapsedTimeMs()} churned through {m} of them")     
            geodes_poss = path.current_max_geodes()
            if geodes_poss > max_geodes:
                max_geodes = geodes_poss
                best_path = path.copy()
            for robot_typ in TYPES:
                if robot_typ==GEODE or path.robots[TYPES.index(robot_typ)] < max_useful_robots[TYPES.index(robot_typ)]:
                    #filter out onward paths that cannot possibly help (any more gatherers doesn't allow any more robot building)
                    can_build, new_path = checkCanBuild(robot_map[robot_typ], path)
                    if can_build:
                        new_paths.append(new_path)
                else:
                    fo+=1
        print(f"\tfiltering by max_useful ignored {fo} new paths")
        paths = new_paths
    return max_geodes, best_path

def printPath(path, minutes, robot_map):
    tracker = BuildOrder.new(minutes)
    b = 0
    for t in range(1,minutes+1):
        tracker.time_left-=1
        print()
        print(f"== Minute {t} ==")
        print(f"collect {tracker.robots} {TYPES}")
        for i in range(4):
            tracker.resources[i]+=tracker.robots[i]
        if b<len(path.built):
            nxt = path.built[b]
            robot = robot_map[nxt]
            if all(robot.resources[i] <= (tracker.resources[i]-tracker.robots[i]) for i in range(4)):
                b+=1
                print(f"Build new {nxt} robot for a cost of {robot.resources}")
                tracker.robots[TYPES.index(nxt)]+=1
                for i in range(4):
                    tracker.resources[i]-=robot.resources[i]
                tracker.built.append(nxt)
        print("TRACKER:",tracker)    
        
    print()
    print("PATH...:",path.current_max_geodes(),path)
    print("TRACKER:",tracker.current_max_geodes(),tracker)
    print()

# # # commented out to speed up part 2 attempts
# # # correct answer: 0:09:10.047979 Total Efficiency is 1659
print("-- == SKIPPING PART ONE CALC == --\n--== ...should really make this a nicer extended function == --\n-- == this is really nasty X-D == --")
# minutes = 24
# total_efficiency = 0
# for bp_id in blueprints:
#     robot_map=blueprints[bp_id]
#     max_geodes, best_path = findMaxGeodes(robot_map,minutes)
#     #printPath(best_path,minutes,robot_map)
#     efficiency = max_geodes * bp_id
#     total_efficiency+=efficiency
#     print(f"\n{elapsedTimeMs()} Blueprint {bp_id} can produce a maximum of {max_geodes} geodes for an efficiency of {efficiency}\n")
# print(f"{elapsedTimeMs()} Total Efficiency is {total_efficiency}")

print(elapsedTimeMs(),"starting prequel to part2")
# the beginnings of an idea to do this more intelligently but it's not finished by any stretch:
#   - calc cost & timing of various robot builds starting with [0,1,1,1] and period to build next geode robot for [0,1,1,2] versus (e.g. [1,1,1,2])
#   - possibly using ratios of costs for each robot type to balance the paths you bother checking?
# ...instead found a way to churn through it just about fast enough to get an answer
# by ignoring paths that added a robot that could not possibly help increase the number of geodes

def tryBackwardCalc(robot_map,minutes):
    max_geodes=0
    max_useful_robots=[max(r.resources[i] for r in robot_map.values()) for i in range(4)]
    print(f"Blueprint has a limit of {max_useful_robots} maximum robots")
    max_useful_robots[3]=minutes # any number of GEODE robots ;)
    to_build=[0,1,1,1]
    res_total=[0,0,0,0]
    for typ_i in range(4):
        resources = robot_map[TYPES[typ_i]].resources
        for j in range(4):
            res_total[j]+=to_build[typ_i]*resources[j]
    print(f"To build {to_build} robots will cost {res_total} and take ?? turns")

    #most you could consume in a given turn of any resource - no point building more than that of the kind of robot

    return max_geodes
minutes = 32
maximums = []
for bp_id in range(1,4):
    try:
        robot_map=blueprints[bp_id]
        max_geodes=tryBackwardCalc(robot_map,minutes)
        print(f"\n{elapsedTimeMs()} Blueprint {bp_id} can produce a maximum of {max_geodes} geodes in {minutes} minutes\n")
    except:
        print("error on index",bp_id)

print(elapsedTimeMs(),"starting part2 - takes AGES...")

# Attempt one ... 6318 was wrong
# bypassing ignore funciton to not try and guess which paths will be usefless... takes longer but sped up with the max_robots removal
# 0:13:22.798495 MAximums of first three after 32 minutes are [9, 27, 28] which have a product of 6804 [CORRECT :D]

minutes = 32
maximums = []
for bp_id in range(1,4):
    robot_map=blueprints[bp_id]
    max_geodes, best_path = findMaxGeodes(robot_map,minutes)
    maximums.append(max_geodes)
    print(f"\n{elapsedTimeMs()} Blueprint {bp_id} can produce a maximum of {max_geodes} geodes in {minutes} minutes\n")
print(f"{elapsedTimeMs()} MAximums of first three after {minutes} minutes are {maximums} which have a product of {math.prod(maximums)}")
