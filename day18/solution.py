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

# class MyClass:
#     def __init__(self, id):
#         self.id=id
#     def __str__(self):
#         return f"MyClass {self.id}"

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    z: int

points=[]
for line in lines:
    x,y,z = map(int,line.split(","))
    point = Point(x,y,z)
    points.append(point)
    print(point)

print(elapsedTimeMs(),"starting part1")

def getExposedArea(points):
    num_points=len(points)
    joins=0
    for i in range(num_points):
        a = points[i]
        for j in range(i,num_points):
            b = points[j]
            if abs(a.x-b.x) + abs(a.y-b.y) + abs(a.z-b.z) == 1:
                joins+=1
    surface_area = num_points*6 - 2*joins
    print(f"counting surface area of {num_points} points based on {joins} joins as {surface_area}")
    return(surface_area)

outer_surface_area = getExposedArea(points)
print(f"{elapsedTimeMs()} outer surface area is {outer_surface_area}")


print(elapsedTimeMs(),"starting part2")
min_point = Point(min(p.x for p in points)-1,min(p.y for p in points)-1,min(p.z for p in points)-1)
max_point = Point(max(p.x for p in points)+1,max(p.y for p in points)+1,max(p.z for p in points)+1)
print("from MIN",min_point,"to MAX",max_point,"covering a total of",abs(max_point.x-min_point.x)*abs(max_point.y-min_point.y)*abs(max_point.z-min_point.z),"points")
blobs=[]
def isAdjacentToBlob(blob,a):
    for b in blob:
        if abs(a.x-b.x) + abs(a.y-b.y) + abs(a.z-b.z) == 1:
            return True
    return False

n=0
for x in range(min_point.x,max_point.x+1):
    for y in range(min_point.y,max_point.y+1):
        for z in range(min_point.z,max_point.z+1):
            n+=1
            if n%1000==0:
                print(f"{n}th point being checked")
            a = Point(x,y,z)
            if a not in points:
                newBlob=True
                i=0
                while newBlob and i<len(blobs):
                    blob = blobs[i]
                    i+=1
                    if isAdjacentToBlob(blob, a):
                        blob.append(a)
                        newBlob = False
                if newBlob:
                    blob = [a]
                    blobs.append(blob)
print("blobs found:",len(blobs))

volume_enclosed=0
inner_surface_area=0
internal_blobs=[]

def isInternal(blob,a,b):
    for p in blob:
        if p.x in [a.x,b.x] or p.y in [a.y,b.y] or p.z in [a.z,b.z]:
            return False
    return True

## TODO merge blobs
def mergeBlobs(blobs):
    overlaps=[]
    seen=set()
    for i in range(len(blobs)-1):
        blobA = blobs[i]
        for j in range(i+1, len(blobs)):
            blobB = blobs[j]
            if any(isAdjacentToBlob(blobB,pointA) for pointA in blobA):
                if i not in seen and j not in seen:
                    overlaps.append([i,j])
                elif i in seen:
                    for overlap in overlaps:
                        if i in overlap:
                            overlap.append(j)
                elif j in seen:
                    for overlap in overlaps:
                        if j in overlap:
                            overlap.append(i)
                seen.update([i,j])
    new_blobs=[]
    for overlap in overlaps:
        blob=[]
        for i in overlap:
            blob+=blobs[i]
        bset=set()
        bset.update(blob)
        blob=list(bset)
        new_blobs.append(blob)
    seen_flat=set()
    # for group in seen:
    #     seen_flat.update(group)
    print("SEEN",seen)
    print("FLAT",seen_flat)
    for i in range(len(blobs)):
        if i not in seen:
            new_blobs.append(blobs[i])
    return(new_blobs)

print(elapsedTimeMs(),"before merging there are",len(blobs),"blobs")
blobs = mergeBlobs(blobs)
print(elapsedTimeMs(),"after merging there are",len(blobs),"blobs")

# testcube is a 3x3x4 object (66 outer area) with a hollow center 1x2 (10 inner area)
n=0
for blob in blobs:
    n+=1
    if isInternal(blob,min_point,max_point):
        internal_blobs.append(blob)
        volume_enclosed+=len(blob)
        surface_area = getExposedArea(blob)
        inner_surface_area+=surface_area
        print(f"Blob {n} out of {len(blobs)} is INTERNAL and has a surface area of {surface_area}")
print(elapsedTimeMs(),len(internal_blobs),"internal blobs with an internal surface area of",inner_surface_area,"leaving an actual external surface area of",outer_surface_area - inner_surface_area)

# well that was painful ... and the code is a mess ... but the answer was found as 2534:
# 0:00:00.007901 starting part1
# counting surface area of 2817 points based on 6256 joins as 4390
# 0:00:00.995270 outer surface area is 4390
# 0:00:00.995288 starting part2
# from MIN Point(x=-1, y=0, z=-1) to MAX Point(x=22, y=22, z=22) covering a total of 11638 points
# 0:00:17.883348 after merging there are 47 blobs
# 0:00:18.119379 46 internal blobs with an internal surface area of 1856 leaving an actual external surface area of 2534

# BROKEN ATTEMPT
# counting surface area of 2817 based on 6256 joins as 4390
# 0:00:00.927329 outer surface area is 4390
# counting surface area of 1367 based on 3326 joins as 1550
# 0:00:11.305563 1 internal blobs with an internal surface area of 1550 leaving an actual external surface area of 2840
# is too high (was losing any blobs not connected to others in the merge)

# 3x3 panel in z=2 used to make layers for testcube test
# 2,2,2
# 2,3,2
# 2,4,2
# 3,2,2
# 3,3,2
# 3,4,2
# 4,2,2
# 4,3,2
# 4,4,2

