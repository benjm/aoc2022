import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()
def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

filename = sys.argv[1]
print_level=0 
if len(sys.argv)>2:
    print_level = int(sys.argv[2])

def readData(filename, decryption_key=1):
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    numbers=[]
    original_i_n={}
    zero_pair=[0,0]
    for i in range(len(lines)):
        number_i = int(lines[i]) * decryption_key
        i_n_pair = (i,number_i)
        numbers.append(i_n_pair)
        original_i_n[i]=i_n_pair
        if number_i == 0:
            zero_pair=i_n_pair
    return numbers,original_i_n,zero_pair

numbers_array,numbers_map,zero_pair = readData(filename)
print(f"{elapsedTimeMs()} read in {len(numbers_array)} numbers")

print(elapsedTimeMs(),"starting part1")

# def reorder(numbers_array,numbers_map,prnt=0):
#     len_numbers = len(numbers_array)
#     if prnt>0: print(f"\n{[i_n[1] for i_n in numbers_array]}\tINITIAL STATE")
#     for i in range(len_numbers):
#         i_n_pair = numbers_map[i]
#         start_i = numbers_array.index(i_n_pair)
#         numbers_array = numbers_array[:start_i]+numbers_array[start_i+1:]
#         delta_i = i_n_pair[1]
#         rotations = abs(delta_i)//len_numbers
#         if rotations > 0:
#             if delta_i < 0:
#                 delta_i+=rotations*len_numbers
#             elif delta_i>0:
#                 delta_i-=rotations*len_numbers
#         mid_i = (start_i+delta_i)
#         end_i=mid_i
#         if i_n_pair[1]<0 and end_i<=0:
#             end_i-=1
#         elif i_n_pair[1]>0 and end_i>=len_numbers:
#             end_i+=1
#         end_i = end_i%len_numbers
#         if (abs(delta_i)%len_numbers==0):
#             end_i=start_i
#         numbers_array = numbers_array[:end_i]+[i_n_pair]+numbers_array[end_i:]
#         if prnt>1: print(f"{[i_n[1] for i_n in numbers_array]}\tmoved {i_n_pair[1]} (actually {delta_i}) from {start_i} to {mid_i} which end up as {end_i}")
#     if prnt>0: print(f"{[i_n[1] for i_n in numbers_array]}\tFINAL STATE")
#     return numbers_array

def deltaIgnoringRotation(delta,circle_back):
    rotations = abs(delta)//circle_back
    if rotations <= 0:
        return delta
    if delta < 0:
        return delta+rotations*circle_back
    elif delta>0:
        return delta-rotations*circle_back

def moveRight(numbers_array, from_i, delta_i_raw):
    len_numbers = len(numbers_array)
    circle_back = len_numbers-1
    delta_i = deltaIgnoringRotation(delta_i_raw,circle_back)
    to_i = from_i + delta_i
    if to_i >= circle_back:
        to_i -= circle_back
    info=f"moveRight n from {from_i} to {to_i} (total {delta_i_raw})"
    if to_i < from_i:
        numbers_array = numbers_array[:to_i]+[numbers_array[from_i]]+numbers_array[to_i:from_i]+numbers_array[from_i+1:]
    else:
        numbers_array = numbers_array[:from_i]+numbers_array[from_i+1:to_i+1]+[numbers_array[from_i]]+numbers_array[to_i+1:]
    return numbers_array,info

def moveLeft(numbers_array, from_i, delta_i_raw):
    len_numbers = len(numbers_array)
    circle_back = len_numbers-1
    delta_i = deltaIgnoringRotation(delta_i_raw,circle_back)
    #next three lines are all that differs from moveRight
    to_i = from_i - delta_i
    if to_i < 1:
        to_i += circle_back
    info=f"moveRight n from {from_i} to {to_i} (total {delta_i_raw})"
    if to_i < from_i:
        numbers_array = numbers_array[:to_i]+[numbers_array[from_i]]+numbers_array[to_i:from_i]+numbers_array[from_i+1:]
    else:
        numbers_array = numbers_array[:from_i]+numbers_array[from_i+1:to_i+1]+[numbers_array[from_i]]+numbers_array[to_i+1:]
    return numbers_array,info


def reorderMK2(numbers_array,numbers_map,prnt=0):
    if prnt>0: print("reorder algorith MKII")
    len_numbers = len(numbers_array)
    if prnt>0: print(f"\n{[i_n[1] for i_n in numbers_array]}\tINITIAL STATE")
    for i in range(len_numbers):
        i_n_pair = numbers_map[i]
        start_i = numbers_array.index(i_n_pair)
        delta_i = i_n_pair[1]
        info = ""
        if delta_i>0:
            numbers_array,info = moveRight(numbers_array, start_i, delta_i)
        elif delta_i<0:
            numbers_array,info = moveLeft(numbers_array, start_i, abs(delta_i))
        else:
            info = f"no movement: stay at {start_i}"
        # else: pass # delta_i == 0 therefore nothing to move
        if prnt>1: print(f"{[i_n[1] for i_n in numbers_array]}\t{info}")
    if prnt>0: print(f"{[i_n[1] for i_n in numbers_array]}\tFINAL STATE")
    return numbers_array

def searchFromTo(numbers_array,zero_pair,index_deltas,prnt=0):
    len_numbers = len(numbers_array)
    current_zero_index = numbers_array.index(zero_pair)
    delta_numbers = []
    actual_indeces = []
    for index_delta in index_deltas:
        actual_index = (current_zero_index + index_delta)%len_numbers
        actual_indeces.append(actual_index)
    for actual_index in actual_indeces:
        i_n_pair = numbers_array[actual_index]
        delta_numbers.append(i_n_pair[1])
    if prnt>0: print(f"\nwith zero at {current_zero_index} and an array of size {len_numbers} the {index_deltas}th indeces work out as {actual_indeces} giving numbers {delta_numbers}")
    return delta_numbers

numbers_array = reorderMK2(numbers_array,numbers_map,print_level)
index_deltas = [1000,2000,3000]
code_numbers = searchFromTo(numbers_array,zero_pair,index_deltas,print_level)
print(f"\n{elapsedTimeMs()} found numbers {code_numbers} at delta indeces {index_deltas} giving a SUM of {sum(code_numbers)}")

# first attempt result was wrong:
# 0:00:00.338358 found numbers [-8003, -9779, -1561] at delta indeces [1000, 2000, 3000] giving a SUM of -19343

# second attempt (after some corrections that confirm working with test input):
# 0:00:00.336309 found numbers [-8003, -9779, 4609] at delta indeces [1000, 2000, 3000] giving a SUM of -13173

# third attempt (after some corrections that were supposed to help with wrap-arounds):
# 0:00:00.339245 found numbers [-277, -9779, 4609] at delta indeces [1000, 2000, 3000] giving a SUM of -5447

# fourth attempt with reorderMK2 (after splitting move left and move right into separate funcitons due to wrapping confusion)
# 0:00:00.267703 found numbers [-8003, 4382, 4609] at delta indeces [1000, 2000, 3000] giving a SUM of 988

print(elapsedTimeMs(),"starting part2")
decryption_key = 811589153

numbers_array,numbers_map,zero_pair = readData(filename, decryption_key)
print(f"{elapsedTimeMs()} read in {len(numbers_array)} numbers again")
if print_level>0:
    print(numbers_array)
for i in range(10):
    numbers_array = reorderMK2(numbers_array,numbers_map,print_level)
index_deltas = [1000,2000,3000]
code_numbers = searchFromTo(numbers_array,zero_pair,index_deltas,print_level)
print(f"\n{elapsedTimeMs()} found numbers {code_numbers} at delta indeces {index_deltas} giving a SUM of {sum(code_numbers)}")
# 0:00:03.548368 found numbers [4670695575515, 2769142190036, 328693606965] at delta indeces [1000, 2000, 3000] giving a SUM of 7768531372516
# already fast enough :-)