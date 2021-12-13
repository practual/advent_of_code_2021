from collections import defaultdict


coords = set()
folds = []

with open('input') as f:
    for coord in f.read().split('\n'):
        if not coord:
            continue
        if coord.startswith('fold'):
            folds.append(tuple(coord.split(' ')[-1].split('=')))
        else:
            coord = coord.split(',')
            coords.add((int(coord[0]), int(coord[1])))

for i, fold in enumerate(folds):
    if fold[0] == 'x':
        fold_dim = 0
    else:
        fold_dim = 1
    fold_val = int(fold[1])

    folded_coords = set()
    for coord in coords:
        folded_coord = [coord[0], coord[1]]
        if coord[fold_dim] > fold_val:
            folded_coord[fold_dim] = 2 * fold_val - coord[fold_dim]
        folded_coords.add(tuple(folded_coord))
    if i == 0:
        print(len(folded_coords))
    coords = folded_coords

max_x = 0
max_y = 0
for coord in coords:
    max_x = max(max_x, coord[0])
    max_y = max(max_y, coord[1])

for y in range(max_y + 1):
    for x in range(max_x + 1):
        if (x, y) in coords:
            print('#', end='')
        else:
            print('.', end='') 
    print('\n', end='')

