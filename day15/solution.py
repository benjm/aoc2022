from dataclasses import dataclass
import sys
import math

filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

# class MyClass:
#     def __init__(self, id):
#         self.id=id
#     def __str__(self):
#         return f"MyClass {self.id}"

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    dist: int
    typ: str

sensors=set()
beacons=set()
for line in lines:
    #Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    l,r=line.split(": closest beacon is at ")
    lxy=l[10:].split(", ")
    rxy=r.split(", ")
    sx,sy=map(lambda peqn: int(peqn.split("=")[1]),lxy)
    bx,by=map(lambda peqn: int(peqn.split("=")[1]),rxy)
    dist = abs(sx-bx) + abs(sy-by)
    sensor = Point(sx,sy,dist,"S")
    beacon = Point(bx,by,0,"B")
    sensors.add(sensor)
    beacons.add(beacon)
    print(sensor)

print("starting part1")

def countCover(y,minx=-math.inf,maxx=math.inf):
    x=set()
    for sensor in sorted(sensors,key=lambda s:str(s.y)+","+str(s.x)):
        dy = abs(sensor.y - y)
        if dy <= sensor.dist:
            dx = sensor.dist-dy
            rx0 = max(minx,sensor.x-dx)
            rx1 = min(maxx,sensor.x+dx)
            newx=range(rx0,rx1+1)
            x.update(newx)
    return x

def countBeacons(y):
    return set(b for b in beacons if b.y==y)

def countNoBeacons(y):
    noBeacons = len(countCover(y)) - len(countBeacons(y))
    print(f"there are {noBeacons} x positions along y={y} where no beacons can be present")

countNoBeacons(10)
countNoBeacons(2000000)

print("starting part2")

def tuningFreq(point):
    return point.x * 4000000 + point.y

@dataclass
class Range:
    start: int
    end: int

def updateGaps(gaps,cover):
    newgaps = []
    for gap in gaps:
        if cover.end < gap.start or cover.start > gap.end:
            #cover is before gap or after gap, gap still exists
            newgaps.append(gap)
        elif cover.start <= gap.start and cover.end >= gap.end:
            # cover completely covers the gap
            pass
        elif cover.start > gap.start and cover.end < gap.end:
            #cover in the middle of the gap
            newgaps.append(Range(gap.start,cover.start-1)) # remaining gap before the cover
            newgaps.append(Range(cover.end+1,gap.end)) # remaining gap after the cover
        elif cover.start <= gap.start:
            newgaps.append(Range(cover.end+1,gap.end)) # remaining gap after the cover
        elif cover.end >= gap.end:
            newgaps.append(Range(gap.start,cover.start-1)) # remaining gap before the cover
    return newgaps

def findGaps(y,minx,maxx):
    gaps=[Range(minx,maxx)]
    for sensor in sorted(sensors,key=lambda s:abs(s.y-y)):
        dy = abs(sensor.y - y)
        if dy <= sensor.dist:
            dx = sensor.dist-dy
            rx0 = sensor.x-dx
            rx1 = sensor.x+dx
            cover = Range(rx0,rx1)
            gaps = updateGaps(gaps,cover)
        if len(gaps)==0:
            return gaps
    return gaps

def findFirstGaps(minxy,maxxy):
    tunings=set()
    for y in range(minxy,maxxy+1):
        if y%100000==0:
            print(f"starting row {y}")
        gaps = findGaps(y,minxy,maxxy)
        for gap in gaps:
            for x in range(gap.start,gap.end+1):
                tuning = tuningFreq(Point(x,y,0,"E"))
                print(f"gap found at {x}, {y} giving tuning {tuning}")
                tunings.add(tuning)
        if len(tunings)>0:
            print("FINISHING EARLY as found at least one gap")
            return tunings

def huntForTuning(minxy,maxxy):
    tunings = findFirstGaps(minxy,maxxy)

huntForTuning(0,20)
huntForTuning(0,4000000)


# ATTEMPT 1: fine for example, not going to cut it scanning 4M rows...!
# def findFirstEmpty(minxy,maxxy):
#     empty = set()
#     delta = 1 + maxxy - minxy
#     for y in range(minxy,maxxy+1):
#         print(f"checking y: {y}")
#         xcover=countCover(y,minxy,maxxy)
#         if len(xcover) < delta:
#             for x in range(minxy,maxxy+1):
#                 if x not in xcover:
#                     empty.add(Point(x,y,0,"E"))
#                     return empty # RETURN EARLY!
#     return empty
# 
#print("tuning freq for TEST:",[tuningFreq(point) for point in findFirstEmpty(0,20)])
#print("tuning freq for REAL:",[tuningFreq(point) for point in findFirstEmpty(0,4000000)])
