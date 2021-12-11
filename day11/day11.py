with open('input') as f:
    octos = [[int(o) for o in row] for row in f.read().split('\n') if row]


neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] 

def get_octo(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return octos[x][y]
    except IndexError:
        return None


def increment_octo(x, y):
    current = get_octo(x, y)
    if current is None:
        return None
    octos[x][y] = current + 1


def check_flash(x, y, has_flashed):
    if get_octo(x, y) is None or get_octo(x, y) < 10 or (x, y) in has_flashed:
        return
    has_flashed.add((x, y))
    for neighbour in neighbours: 
        increment_octo(x + neighbour[0], y + neighbour[1])
    for neighbour in neighbours:
        check_flash(x + neighbour[0], y + neighbour[1], has_flashed)

def run_step():
    has_flashed = set()
    for x, row in enumerate(octos):
        for y, col in enumerate(octos):
            increment_octo(x, y) 
    for x, row in enumerate(octos):
        for y, col in enumerate(octos):
            check_flash(x, y, has_flashed)
    for x, row in enumerate(octos):
        for y, col in enumerate(octos):
            if octos[x][y] > 9:
                octos[x][y] = 0
    return len(has_flashed)

octos_copy = [[col for col in row] for row in octos]
num_flashes = 0
for step in range(100):
    num_flashes += run_step()
print(num_flashes)

octos = octos_copy
step_num = 0
while True:
    step_num += 1
    num_flashes = run_step()
    if num_flashes == 100:
        break
print(step_num)

