with open('input') as f:
    data = [row for row in f.read().split('\n') if row]

def make_mask(data):
    counter = None
    for row in data:
        if counter is None:
            counter = [0] * len(row)
        for i in range(len(row)):
            counter[i] += 1 if int(row[i]) else -1

    return [int(i >= 0) for i in counter]

counter = make_mask(data)
gamma = int(''.join(map(str, counter)), 2)
epsilon = int(''.join(map(lambda i: str(int(not i)), counter)), 2)
print(gamma * epsilon)

o2_values = [row for row in data]
filter_col = 0
while len(o2_values) > 1:
    counter = make_mask(o2_values)
    o2_values = list(filter(lambda value: int(value[filter_col]) == counter[filter_col], o2_values))
    filter_col += 1

co2_values = [row for row in data]
filter_col = 0
while len(co2_values) > 1:
    counter = make_mask(co2_values)
    co2_values = list(filter(lambda value: int(value[filter_col]) != counter[filter_col], co2_values))
    filter_col += 1

print(int(o2_values[0], 2) * int(co2_values[0], 2))

