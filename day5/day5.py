import re
from collections import defaultdict


with open('input') as f:
    lines = []
    for line in f.read().split('\n'):
        if not line:
            break
        match = re.match('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)', line)
        from_coords = (int(match[1]), int(match[2]))
        to_coords = (int(match[3]), int(match[4]))
        lines.append((from_coords, to_coords))


def count_overlaps(ocean_floor):
    overlaps = 0
    for lines in ocean_floor.values():
        if lines > 1:
            overlaps += 1
    return overlaps


def get_next(start, end, current):
    if start == end:
        return start
    if current == end:
        return None
    return current + 1 if start < end else current - 1


def map_floor(with_diagonal):
    ocean_floor = defaultdict(int)
    for line in lines:
        from_coords, to_coords = line
        if not with_diagonal and (from_coords[0] != to_coords[0] and from_coords[1] != to_coords[1]):
            continue
        current_x, current_y = from_coords
        while current_x and current_y:
            ocean_floor[(current_x, current_y)] += 1
            current_x = get_next(from_coords[0], to_coords[0], current_x)
            current_y = get_next(from_coords[1], to_coords[1], current_y)
    return ocean_floor
 

print(count_overlaps(map_floor(False)))
print(count_overlaps(map_floor(True)))

