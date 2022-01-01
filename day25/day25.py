east_herd = set()
south_herd = set()
max_x, max_y = 0, 0

with open('input') as f:
    for x, row in enumerate(f.read().split('\n')):
        if not row:
            break
        max_x = max(max_x, x + 1)
        for y, col in enumerate(row):
            max_y = max(max_y, y + 1)
            if col == '>':
                east_herd.add((x, y))
            elif col == 'v':
                south_herd.add((x, y))


def take_step(east_herd, south_herd):
    num_moves = 0
    new_east_herd = set()
    for cucumber in east_herd:
        cucumber_in_front = (cucumber[0], (cucumber[1] + 1) % max_y)
        if cucumber_in_front not in east_herd and cucumber_in_front not in south_herd:
            new_east_herd.add(cucumber_in_front)
            num_moves += 1
        else:
            new_east_herd.add(cucumber)
    new_south_herd = set()
    for cucumber in south_herd:
        cucumber_in_front = ((cucumber[0] + 1) % max_x, cucumber[1])
        if cucumber_in_front not in new_east_herd and cucumber_in_front not in south_herd:
            new_south_herd.add(cucumber_in_front)
            num_moves += 1
        else:
            new_south_herd.add(cucumber)
    return new_east_herd, new_south_herd, num_moves


steps = 0
num_moves = 1
while num_moves > 0:
    east_herd, south_herd, num_moves = take_step(east_herd, south_herd)
    steps += 1
print(steps)

