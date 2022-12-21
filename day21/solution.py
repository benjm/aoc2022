import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()
def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

@dataclass
class Monkey:
    name: str
    left_monkey: str
    right_monkey: str
    op: str
    result: int

def processLines(lines):
    monkeys={}
    for line in lines:
        name,right = line.split(": ")
        split_right=right.split()
        left_monkey=right_monkey=op=result=None
        if len(split_right)==3:
            left_monkey,op,right_monkey=split_right
        else:
            result=int(right)
        monkey=Monkey(name,left_monkey,right_monkey,op,result)
        monkeys[monkey.name]=monkey
    return monkeys

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

ROOT="root"
monkeys = readFile()

print(elapsedTimeMs(),"starting part1")

def doMonkeyCalc(left_result, op, right_result, monkey, print_in_full=False):
    if print_in_full: print(f"\twill calculate {left_result} {op} {right_result}")
    result = None
    if monkey.op=="+":
        result = left_result + right_result
    elif monkey.op=="-":
        result = left_result - right_result
    elif monkey.op=="*":
        result = left_result * right_result
    elif monkey.op=="/":
        if right_result == 0 or left_result%right_result>0:
            if print_in_full:
                print(f"DIVISION ERROR for {monkey}")
        else:
            result = left_result // right_result
    return result

def getResult(monkeys,name,update_result=True,print_in_full=False):
    monkey = monkeys[name]
    result = monkey.result
    if print_in_full: print(f"getting result for monkey {name}: {monkey}")
    try:
        if result != None:
            if print_in_full: print(f"\t direct return {result}")
            return result
        left_result = getResult(monkeys,monkey.left_monkey,update_result,print_in_full)
        right_result = getResult(monkeys,monkey.right_monkey,update_result,print_in_full)
        result = doMonkeyCalc(left_result,monkey.op,right_result,monkey,print_in_full)
        if result != None and update_result:
            monkey.result=result
            if print_in_full: print(f"UPDATED RESULT on {monkey}")
    except:
        if print_in_full: print(f"\tEXCEPTION processing {name}")
    if print_in_full: print(f"\treturning {result} for monkey {name}")
    return result

result = getResult(monkeys,ROOT)
print(f"{elapsedTimeMs()} {ROOT} shouts {result}")

print(elapsedTimeMs(),"starting part2")
# ROOT is doing an equality check
# humn is YOU and YOU need to shout a number to make the equality check pass

YOU = "humn"
monkeys = readFile() #reset!
monkeys[YOU].result=None
getResult(monkeys,ROOT) # update anything that can be updated
print(elapsedTimeMs(),"number of monkeys without a known result:",sum(1 for m in monkeys if not monkeys[m].result))

# there is no doubt a better way to represent the equality than as a string that gets re-interpreted but it'll do fine for now and is actually pretty fast
def getEquality(monkeys, monkey_name):
    monkey=monkeys[monkey_name]
    if monkey.result != None:
        return f"{monkey.result}"
    elif monkey_name == YOU:
        return f"({YOU})"
    return f"({getEquality(monkeys,monkey.left_monkey)} {monkey.op} {getEquality(monkeys,monkey.right_monkey)})"

def printEquality(monkeys,ROOT):
    left_monkey = monkeys[monkeys[ROOT].left_monkey]
    right_monkey = monkeys[monkeys[ROOT].right_monkey]
    left_equality = getEquality(monkeys, left_monkey.name)
    right_equality = getEquality(monkeys, right_monkey.name)
    if "(" in left_equality:
        if "(" in right_equality:
            print("ERROR!!! Both equalities were equations")
            return left_equality, right_equality
        return int(right_equality), left_equality
    return int(left_equality), right_equality

result, equality = printEquality(monkeys,ROOT)
print(f"vv EQUALITY vv\n{equality}\n==== IS EQUAL TO ====\n{result}\n^^ EQUALITY RESULT ^^")

# ((209 + (844 + (56210878171817 - (2 * (576 + ((((968 + ((35 + (((((2 * (((190 + (2 * ((18 * (206 + ((((((((((((5 * (((341 + (2 * (((373 + (20 * ((((98 + ((959 + (((11 * (((180 + ((124 + (((((2 * (((485 + ((17 * (humn - 437)) + 422)) / 2) + 176)) - 626) / 2) - 801) * 2)) / 3)) / 2) - 454)) - 187) / 6)) * 3)) + 733) / 9) - 608))) / 3) - 944))) / 5) - 904)) + 708) * 2) - 228) / 9) + 451) + 709) / 2) - 1) * 4) - 201) / 7))) - 203))) / 12) - 907)) + 996) / 4) - 754) * 5)) / 2)) / 3) - 948) * 2)))))) / 2)
# ==== IS EQUAL TO ====
# 13751780524553

def leftEqualityCalc(left_val,op,result,equality):
    if op=="+":
        result = result - left_val
    elif op=="-":
        result = left_val - result
    elif op=="*":
        if left_val==0 or result%left_val>0:
            print(f"DIVISION (left *) ERROR {equality} = {result}")
        result = result // left_val
    elif op=="/":
        if result==0 or left_val%result>0:
            print(f"DIVISION (left /) ERROR {equality} = {result}")
        result = left_val // result
    else:
        print(f"OPERATOR (left) ERROR {equality} = {result}")
    return result

def rightEqualityCalc(right_val,op,result,equality):
    if op=="+":
        result = result - right_val
    elif op=="-":
        result = right_val + result
    elif op=="*":
        if right_val==0 or result%right_val>0:
            print(f"DIVISION (left *) ERROR {equality} = {result}")
        result = result // right_val
    elif op=="/":
        result = right_val * result
    else:
        print(f"OPERATOR (left) ERROR {equality} = {result}")
    return result

def reduceBackwards(equality,result,print_in_full=False):
    if print_in_full: print(f"{equality} = {result}")
    if equality[0]=="(" and equality[-1]==")":
        equality = equality[1:-1]
    if equality == YOU:
        print(equality,"=",result)
        return result
    if equality[0].isdigit():
        i=0
        while i<len(equality) and equality[i]!="(":
            i+=1
        left=equality[:i].split()
        left_val=int(left[0])
        op=left[1]
        result=leftEqualityCalc(left_val,op,result,equality)
        equality = equality[i:]
        return reduceBackwards(equality,result)
    if equality[-1].isdigit():
        i=len(equality)-1
        while i>=0 and equality[i]!=")":
            i-=1
        i+=1
        right=equality[i:].split()
        right_val=int(right[-1])
        op=right[-2]
        result=rightEqualityCalc(right_val,op,result,equality)
        return reduceBackwards(equality[:i],result)
    else:
        print(f"SCANNING ERROR |{equality}| = {result}")
        exit()

human_shouts = reduceBackwards(equality,result,print_in_full=False)
print(elapsedTimeMs(),"The human shouts",human_shouts)
# 0:00:00.004603 The human shouts 3916936880448 correct. LEss than a second is better than 64 years (see below)

# # DISCOUNTED BRUTE FORCE APPROACH...
# # Blunt search every time took 15min to assess up to 2.5M ...
# # original run was number 41857219607906 which would take ~500 years (hahaha) to reach at that rate
# # running update on monkeys first sped this up, reaching 2.5M after 2min ... down to maybe ~64 years
# def runUgly():
#     root_monkey=monkeys[ROOT]
#     monkeys[YOU].result=0
#     left = getResult(monkeys,root_monkey.left_monkey,update_result=False)
#     right = getResult(monkeys,root_monkey.right_monkey,update_result=False)
#     while not left or not right or left != right:
#         monkeys[YOU].result+=1
#         left = getResult(monkeys,root_monkey.left_monkey,update_result=False)
#         right = getResult(monkeys,root_monkey.right_monkey,update_result=False)
#         if monkeys[YOU].result%100000==0:
#             print(elapsedTimeMs(),"up to",monkeys[YOU].result)
#     print(elapsedTimeMs(),"UGLY SOLUTION",monkeys[YOU].result)
# runUgly()