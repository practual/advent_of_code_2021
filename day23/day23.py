with open('input') as f:
    rooms = [[], [], [], []]
    room_ptr = 0
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n')
        for c in line:
            if c in ['A', 'B', 'C', 'D']:
                rooms[room_ptr].append(c)
                room_ptr = (room_ptr + 1) % 4



multipliers = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

room_junctions = ['c2', 'c4', 'c6', 'c8']


def is_room_sorted(burrow, room_size, room_number, is_full=False):
    # Return True if the only occupants of a given room are correctly sorted there.
    # (and hence the room can be entered by other pods of that type)
    correct_pod = chr(room_number + 65)
    for s in range(room_size):
        occupant = burrow['r' + str(room_number) + str(s)]
        if occupant != correct_pod and (occupant != '' or is_full):
            return False
    return True


def get_distance_room_to_corridor(burrow, start, ignore_blockage):
    distance = 0
    room_number = int(start[1])
    room_slot = int(start[2])
    for slot in range(room_slot - 1, -1, -1):
        if not ignore_blockage and burrow['r' + str(room_number) + str(slot)] != '':
            return 0
        distance += 1
    if not ignore_blockage and burrow[room_junctions[room_number]] != '':
        return 0
    distance += 1
    return distance


def get_distance_corridor_to_corridor(burrow, start, end, ignore_blockage):
    distance = 0
    c_start = int(''.join(start[1:]))
    c_end = int(''.join(end[1:]))
    range_start = min(c_start, c_end) + 1
    range_end = max(c_start, c_end) + 1
    for c in range(min(c_start, c_end), max(c_start, c_end) + 1):
        if 'c' + str(c) == start:
            continue
        if not ignore_blockage and burrow['c' + str(c)] != '':
            return 0
        distance += 1
    return distance


def get_distance_corridor_to_room(burrow, room_number, room_size, ignore_blockage):
    if ignore_blockage:
        return 1, 0
    if not is_room_sorted(burrow, room_size, room_number):
        return 0, None
    if is_room_sorted(burrow, room_size, room_number, is_full=True):
        return 0, None
    distance = 0
    for slot in range(room_size):
        occupant = burrow['r' + str(room_number) + str(slot)]
        if occupant != '':
            return distance, slot - 1
        distance += 1
    return distance, room_size - 1
 

def get_distance(burrow, room_size, start, end, ignore_blockage=False):
    distance = 0
    if start.startswith('r'):
        r_to_c = get_distance_room_to_corridor(burrow, start, ignore_blockage)
        if not r_to_c:
            return 0, None
        distance += r_to_c
        start = room_junctions[int(start[1])]
    if end.startswith('c'):
        c_to_c = get_distance_corridor_to_corridor(burrow, start, end, ignore_blockage)
        if not c_to_c:
            return 0, None
        distance += c_to_c
        return distance, None
    end_room_num = int(end[1])
    c_to_c = get_distance_corridor_to_corridor(burrow, start, room_junctions[end_room_num], ignore_blockage)
    if not c_to_c:
        return 0, None
    distance += c_to_c
    c_to_r, slot = get_distance_corridor_to_room(burrow, end_room_num, room_size, ignore_blockage)
    if not c_to_r:
        return 0, None
    distance += c_to_r
    return distance, slot


def find_locations(burrow, room_size, start):
    occupant = burrow[start]
    target_room = ord(occupant) - 65
    if start.startswith('r'):
        if is_room_sorted(burrow, room_size, int(start[1])):
            return []
        #current_room_pod = chr(65 + int(start[1]))
        #if all(burrow[''.join(start[:2]) + str(s)] in [current_room_pod, ''] for s in range(room_size)):
        #    return []
        possible_locations = ['r' + str(target_room), 'c0', 'c1', 'c3', 'c5', 'c7', 'c9', 'c10']
    else:
        possible_locations = ['r' + str(target_room)]
    locations = []
    for location in possible_locations:
        distance, slot = get_distance(burrow, room_size, start, location)
        if not distance:
            continue
        locations.append((location + (str(slot) if location[0] == 'r' else ''), distance * multipliers[occupant]))
    return locations


def estimate_remaining_cost(burrow, room_size):
    total_cost = 0
    for location, occupant in burrow.items():
        if occupant == '':
            continue
        target_room = ord(occupant) - 65
        if location.startswith('r') and int(location[1]) == target_room:
            continue
        distance, _ = get_distance(burrow, room_size, location, 'r' + str(target_room), True)
        total_cost += distance * multipliers[occupant]
    return total_cost


def check_position(burrow, cost):
    burrow_keys = []
    for key in sorted(location for location, occupant in burrow.items() if occupant != ''):
        burrow_keys.append('{}:{}'.format(key, burrow[key]))
    burrow_key = tuple(burrow_keys)
    if burrow_key not in position_costs or position_costs[burrow_key] > cost:
        position_costs[burrow_key] = cost
        return True
    return False


def check_burrow(burrow, room_size):
    for r in range(4):
        for s in range(room_size):
            if burrow['r' + str(r) + str(s)] != chr(65 + r):
                return False
    return True


def arrange(burrow, room_size, cost, best_cost,last_move):
    if not check_position(burrow, cost):
        # We have already been in this arrangement but with a better cost.
        # No benefit to continuing.
        return best_cost
    if cost + estimate_remaining_cost(burrow, room_size) >= best_cost:
        # No path from here will improve on the best cost.
        # No benefit to continuing.
        return best_cost
    if check_burrow(burrow, room_size):
        # Burrow is completely sorted! Nothing to do from here.
        return cost
    for location, occupant in burrow.items():
        if occupant == '' or location == last_move:
            continue
        for new_location, new_cost in find_locations(burrow, room_size, location):
            new_burrow = burrow.copy()
            new_burrow[location] = ''
            new_burrow[new_location] = occupant
            best_cost = min(best_cost, arrange(new_burrow, room_size, cost + new_cost, best_cost, new_location))
    return best_cost


burrow = {'c' + str(c): '' for c in range(11)}
for r, room in enumerate(rooms):
    for s, pod in enumerate(room):
        burrow['r' + str(r) + str(s)] = pod
position_costs = {}
print(arrange(burrow, len(rooms[0]), 0, float('inf'), None))


rooms = [
    [rooms[0][0]] + ['D', 'D'] + [rooms[0][1]],
    [rooms[1][0]] + ['C', 'B'] + [rooms[1][1]],
    [rooms[2][0]] + ['B', 'A'] + [rooms[2][1]],
    [rooms[3][0]] + ['A', 'C'] + [rooms[3][1]],
]

burrow = {'c' + str(c): '' for c in range(11)}
for r, room in enumerate(rooms):
    for s, pod in enumerate(room):
        burrow['r' + str(r) + str(s)] = pod
position_costs = {}
print(arrange(burrow, len(rooms[0]), 0, float('inf'), None))

