import sys
import math
from dataclasses import dataclass
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

# class MyClass:
#     def __init__(self, id):
#         self.id=id
#     def __str__(self):
#         return f"MyClass {self.id}"

# @dataclass(unsafe_hash=True)
# class Point:
#     x: int
#     y: int

print("starting part1")


# print("starting part2")
