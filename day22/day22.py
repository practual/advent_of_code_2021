import itertools


with open('input') as f:
    instructions = f.read().split('\n')


def get_limited_range(raw):
    min_max = tuple(map(int, raw.split('=')[1].split('..')))
    assert min_max[0] < min_max[1]
    if min_max[1] < -50 or min_max[0] > 50:
        return None
    return max(min_max[0], -50), min(min_max[1], 50)


def get_range(raw):
    return tuple(map(int, raw.split('=')[1].split('..')))


def update_reactor(reactor, direction, coords):
    for x in range(coords[0][0], coords[0][1] + 1):
        for y in range(coords[1][0], coords[1][1] + 1):
            for z in range(coords[2][0], coords[2][1] + 1):
                if direction == 'off':
                    try:
                        reactor.remove((x, y, z))
                    except KeyError:
                        pass
                else:
                    reactor.add((x, y, z))


reactor = set()
for instruction in instructions:
    if not instruction:
        continue
    direction, coords = instruction.split(' ')
    x_range, y_range, z_range = map(get_limited_range, coords.split(','))
    if not all((x_range, y_range, z_range)):
        continue
    update_reactor(reactor, direction, (x_range, y_range, z_range))
print(len(reactor))


def union(volumes, v, direction):
    volumes_to_add = set()
    if direction == 'on':
        volumes_to_add.add((1, (v,)))
    for weight, volume in volumes:
        if not intersect(volume + (v,)):
            continue
        volumes_to_add.add((-1 * weight, tuple(sorted(volume + (v,)))))
    volumes |= volumes_to_add
    return volumes


def find_overlap_coords(c1, c2):
    if any(c2[i][0] < c1[i][0] and c2[i][1] < c1[i][0] or c2[i][0] > c1[i][1] and c2[i][1] > c1[i][1] for i in range(3)):
        return
    return tuple((max(c1[i][0], c2[i][0]), min(c1[i][1], c2[i][1])) for i in range(3))


def find_intersect_part(volumes):
    canonical_order = sorted(volumes)
    for r in range(len(volumes), 0, -1):
        for c in itertools.combinations(canonical_order, r=r):
            if c in volume_coords:
                return c, volume_coords[c]


def intersect(volumes):
    remaining_volumes = set(volumes)
    known_coords = []
    intersected_volumes = ()
    intersected = None
    while len(remaining_volumes):
        known_volumes, known_coords = find_intersect_part(tuple(remaining_volumes))
        if known_coords is None:
            volume_coords[tuple(sorted(volumes))] = None
            return None
        intersected_volumes += known_volumes
        if intersected is None:
            intersected = known_coords
        else:
            intersected = find_overlap_coords(intersected, known_coords)
            volume_coords[tuple(sorted(intersected_volumes))] = intersected
        remaining_volumes -= set(known_volumes)
    return intersected


print('This will take a couple of minutes...')
volumes = set()
volume_coords = {}
for v, instruction in enumerate(instructions):
    if not instruction:
        continue
    direction, coords = instruction.split(' ')
    x_range, y_range, z_range = map(get_range, coords.split(','))
    volume_coords[(v,)] = (x_range, y_range, z_range)
    if not volumes:
        if direction == 'off':
            continue
        volumes.add((1, (v,)))
    else:
        volumes = union(volumes, v, direction)

total_volume = 0
for weight, volume in volumes:
    coords = volume_coords[volume]
    total_volume += ((abs(coords[0][1] - coords[0][0]) + 1) * (abs(coords[1][1] - coords[1][0]) + 1) * (abs(coords[2][1] - coords[2][0]) + 1)) * weight
print(total_volume)

