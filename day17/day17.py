with open('input') as f:
    target_coords = f.readline().strip('\n').split(' ')
    target_x = tuple(map(lambda x: int(x.strip(',')), target_coords[2].split('=')[1].split('..')))
    target_y = tuple(map(int, target_coords[3].split('=')[1].split('..')))


def test_velocity(v):
    max_y = 0
    pos = (0, 0)
    hit_target = False
    while pos[0] < target_x[1] and pos[1] > target_y[0]:
        pos = (pos[0] + v[0], pos[1] + v[1])
        v_x_delta = 0
        if v[0] > 0:
            v_x_delta = -1
        elif v[0] < 0:
            v_x_delta = 1
        v = (v[0] + v_x_delta, v[1] - 1) 
        max_y = max(max_y, pos[1])
        if pos[0] >= target_x[0] and pos[0] <= target_x[1] and pos[1] >= target_y[0] and pos[1] <= target_y[1]:
            hit_target = True
    return max_y if hit_target else None


max_y = 0
num_hits = 0
for v_x in range(1000):
    for v_y in range(-1000, 1000):
        max_y_for_velocity = test_velocity((v_x, v_y))
        if max_y_for_velocity is not None:
            num_hits += 1
            max_y = max(max_y, max_y_for_velocity)
print(max_y)
print(num_hits)
 
