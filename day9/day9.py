with open('input') as f:
    height_map = [[int(j) for j in i] for i in f.read().split('\n') if i]


def get_height(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return height_map[x][y]
    except IndexError:
        return None


def test_neighbours(x, y):
    middle = get_height(x, y)
    top = get_height(x-1, y)
    right = get_height(x, y+1)
    bottom = get_height(x+1, y)
    left = get_height(x, y-1)
    return all([neighbour is None or middle < neighbour for neighbour in [top, right, bottom, left]])


risk = 0
for x, row in enumerate(height_map):
    for y, val in enumerate(row):
        if test_neighbours(x, y):
            risk += val + 1
print(risk)


def get_basin_size(x, y, checked_coords):
    if (x, y) in checked_coords:
        return 0
    checked_coords.add((x, y))
    current_height = get_height(x, y)
    if current_height is None or current_height == 9:
        return 0
    return (
        1 +
        get_basin_size(x - 1, y, checked_coords) +
        get_basin_size(x, y + 1, checked_coords) +
        get_basin_size(x + 1, y, checked_coords) +
        get_basin_size(x, y - 1, checked_coords)
    )

basin_sizes = []
for x in range(len(height_map)):
    for y in range(len(height_map[0])):
        if test_neighbours(x, y):
            basin_sizes.append(get_basin_size(x, y, set()))

basin_sizes = sorted(basin_sizes)
print(basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])

