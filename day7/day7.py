with open('input') as f:
    positions = sorted(map(int, f.readline().strip('\n').split(',')))

if len(positions) % 2:
    median = positions[(len(positions) - 1) // 2]
else:
    median = (positions[len(positions) // 2 - 1] + positions[len(positions) // 2]) // 2

print(sum(abs(position - median) for position in positions))

mean = sum(positions) // len(positions)
print(sum(abs(position - mean) * (abs(position - mean) + 1) // 2 for position in positions))

