with open('input') as f:
    data = [int(row) for row in f.read().split('\n') if row]

increases = 0
prev_depth = 0
for depth in data:
    if prev_depth and depth > prev_depth:
        increases += 1
    prev_depth = depth

print(increases) 

increases = 0
prev_depth = 0
for i in range(2, len(data)):
    current_window = data[i-2] + data[i-1] + data[i]
    if prev_depth and current_window > prev_depth:
        increases += 1
    prev_depth = current_window

print(increases)

