with open('input') as f:
    data = [row.split(' ') for row in f.read().split('\n') if row]

h, v = 0, 0
for inst in data:
    direction = inst[0]
    distance = int(inst[1])
    if direction == 'forward':
        h += distance
    elif direction == 'up':
        v -= distance
    elif direction == 'down':
        v += distance

print(h * v)

h, v, a = 0, 0, 0
for inst in data:
    command = inst[0]
    operand = int(inst[1])
    if command == 'forward':
        h += operand
        v += operand * a
    elif command == 'up':
        a -= operand
    elif command == 'down':
        a += operand

print(h * v)

