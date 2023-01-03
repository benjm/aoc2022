import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

data = readFile()

# @dataclass(unsafe_hash=True)
# class Point:
#     x: int
#     y: int

print(elapsedTimeMs(),"starting part1")

basemap={
    "=":-2,
    "-":-1,
    "0":0,
    "1":1,
    "2":2
}
decmap={}
for b in basemap:
    d=basemap[b]
    decmap[d]=b

def baseToDec(base):
    dec=0
    pfive=1
    for b in base[::-1]:
        d=basemap[b]*pfive
        dec+=d
        pfive*=5
    return dec

def decToBase(dec):
    base=""
    carry=0
    lastPfive=1
    pfive=5
    while dec>0:
        remfive = dec%pfive
        if remfive>(2*lastPfive):
            remfive-=pfive
        i_five=remfive//lastPfive
        #print(f"{dec}%{pfive}==>{remfive} (inverted: {remfive>(2*lastPfive)}) -- index: {i_five}")
        dec-=remfive
        lastPfive=pfive
        pfive*=5
        base=decmap[i_five]+base
    return base

def sumUpLines(bases):
    totalDecimal = 0
    for base in bases:
        decimal = baseToDec(base)
        totalDecimal+=decimal
    return totalDecimal

bases = readFile()
totalDecimal = sumUpLines(bases)
totalBase = decToBase(totalDecimal)
print(elapsedTimeMs(),totalDecimal,totalBase)

# print(elapsedTimeMs(),"starting part2")
