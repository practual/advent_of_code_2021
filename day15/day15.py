import sys
from collections import defaultdict


sys.setrecursionlimit(15000)

with open('input') as f:
    cave = [[int(col) for col in row] for row in f.read().split('\n') if row]

risk = defaultdict(int)

def get_risk(x, y):
    if x < 0 or y < 0:
        return None
    if (0, 0) not in risk:
        return 0
    try:
        return cave[x][y]
    except IndexError:
        return None


def get_current_risk(x, y):
    if (x, y) in risk:
        return risk[(x, y)]
    return 9 * (x + y) + 1

def explore(x, y, current_risk, direction):
    risk_of_entering = get_risk(x, y) 
    if risk_of_entering is None:
        return
    risk_for_position = current_risk + risk_of_entering
    if risk_for_position >= get_current_risk(x, y):
        return
    risk[(x, y)] = risk_for_position
    if direction != 1:
        explore(x - 1, y, risk_for_position, 4)
    if direction != 2:
        explore(x, y - 1, risk_for_position, 3)
    if direction != 3:
        explore(x, y + 1, risk_for_position, 2)
    if direction != 4:
        explore(x + 1, y, risk_for_position, 1)


explore(0, 0, 0, 2)
print(get_current_risk(len(cave) - 1, len(cave[0]) - 1))

big_cave = []
for i in range(5):
    for row in cave:
        big_cave.append([])
    for j in range(5):
        for r, row in enumerate(cave):
            for col in row:
                big_cave[i * len(cave) + r].append((col - 1 + i + j) % 9 + 1)
cave = big_cave
risk = defaultdict(int)

explore(0, 0, 0, 2)
print(get_current_risk(len(cave) - 1, len(cave[0]) - 1))

