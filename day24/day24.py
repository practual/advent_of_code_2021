with open('input') as f:
    instructions = f.read().split('\n')

xs = []
ys = []

for block in range(14):
    xs.append(int(instructions[block * 18 + 5].split(' ')[2]))
    ys.append(int(instructions[block * 18 + 15].split(' ')[2]))

ys_to_balance = []
balancing_pairs = []
for i, (x, y) in enumerate(zip(xs, ys)):
    if x <= 0:
        balancing_pairs.append((ys_to_balance[-1], (i, x)))
        ys_to_balance = ys_to_balance[:-1]
    else:
        ys_to_balance.append((i, y))

biggest_model = {}
smallest_model = {}

for y, x in balancing_pairs:
    diff = y[1] + x[1]
    biggest_model[y[0]] = 9 - max(diff, 0)
    biggest_model[x[0]] = 9 + min(diff, 0)
    smallest_model[y[0]] = 1 - min(diff, 0)
    smallest_model[x[0]] = 1 + max(diff, 0)

print(''.join([str(biggest_model[i]) for i in range(14)]))
print(''.join([str(smallest_model[i]) for i in range(14)]))

