import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

decode_shape = {
    "A":"R",
    "B":"P",
    "C":"S",
    "X":"R",
    "Y":"P",
    "Z":"S"
}
beats = {
    "R":"P",
    "P":"S",
    "S":"R"
}
loses = {
    "R":"S",
    "P":"R",
    "S":"P"
}
scoring = {
    "Win":6,
    "Lose":0,
    "Draw":3,
    "R":1,
    "P":2,
    "S":3
}

score = 0
for line in lines:
    opp_encoded,me_encoded = line.split()
    opp = decode_shape[opp_encoded]
    me = decode_shape[me_encoded]
    outcome = [["Draw","Win"][me == beats[opp]],"Lose"][opp == beats[me]]
    score+=scoring[me]+scoring[outcome]
    #print(line,"-->",opp,me,"-->",outcome,score)

print(score)

print("starting part2")

decode_outcome = {
    "X":"Lose",
    "Y":"Draw",
    "Z":"Win"
}

score = 0
for line in lines:
    opp_encoded,me_instruct = line.split()
    opp = decode_shape[opp_encoded]
    outcome = decode_outcome[me_instruct]
    me = [[opp,loses[opp]][outcome == "Lose"],beats[opp]][outcome == "Win"]
    score+=scoring[me]+scoring[outcome]
    #print(line,"-->",opp,me,"-->",outcome,score)

print(score)
