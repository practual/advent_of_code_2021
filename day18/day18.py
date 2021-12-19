import itertools


with open('input') as f:
    numbers_raw = f.read().split('\n')

def prepare_number(raw_number):
    number = []
    for c in raw_number:
        if c in ['[', ']']:
            number.append(c)
        elif c != ',':
            number.append(int(c))
    return number


numbers = list(map(prepare_number, (raw_number for raw_number in numbers_raw if raw_number)))

def process_explode(number, left_num_idx, pair_r_idx):
    if left_num_idx is not None:
        left_value = number[left_num_idx] + number[pair_r_idx - 1]
        number = number[:left_num_idx] + [left_value] + number[left_num_idx + 1:]
    right_num_idx = None
    for pointer, c in enumerate(number[pair_r_idx + 2:]):
        if c not in ['[', ']']:
            right_num_idx = pair_r_idx + 2 + pointer
            break
    if right_num_idx is not None:
        right_value = number[right_num_idx] + number[pair_r_idx]
        number = number[:right_num_idx] + [right_value] + number[right_num_idx + 1:]
    return number[:pair_r_idx - 2] + [0] + number[pair_r_idx + 2:]


def explode(number):
    left_num_idx = None
    pair_l = None
    pair_count = 0
    for pointer, c in enumerate(number):
        if c == '[':
            pair_count += 1
            pair_l = None
        elif c == ']':
            pair_count -= 1
        elif pair_count <= 4:
            left_num_idx = pointer
        elif pair_l is None:
            pair_l = c
        else:
            return process_explode(number, left_num_idx, pointer), True
    return number, False


def split(number):
    for pointer, c in enumerate(number):
        if c not in ['[', ']'] and c >= 10:
            split_val = ['[', c // 2, c // 2 + c % 2, ']']
            return number[:pointer] + split_val + number[pointer + 1:], True
    return number, False


def reduce(number):
    while True:
        number, did_explode = explode(number)
        if did_explode:
            continue
        number, did_split = split(number)
        if did_split:
            continue
        break
    return number
 

def addition(a, b):
    return reduce(['['] + a + b + [']'])


def nest_one(number):
    pair_l = None
    for pointer, c in enumerate(number):
        if not isinstance(c, list) and c in ['[', ']']:
            pair_l = None
        elif pair_l is None:
            pair_l = c
        else:
            return number[:pointer - 2] + [[pair_l, c]] + number[pointer + 2:], True
    return number, False


def nest(number):
    more_to_nest = True
    while more_to_nest:
        number, more_to_nest = nest_one(number)
    return number[0]


def get_magnitude(number):
    magnitude = 0
    if isinstance(number[0], int):
        magnitude += 3 * number[0]
    else:
        magnitude += 3 * get_magnitude(number[0])
    if isinstance(number[1], int):
        magnitude += 2 * number[1]
    else:
        magnitude += 2 * get_magnitude(number[1])
    return magnitude


answer = numbers[0]
for number in numbers[1:]:
    answer = addition(answer, number)
print(get_magnitude(nest(answer)))

max_magnitude = 0
for comb in itertools.combinations(numbers, 2):
    max_magnitude = max(max_magnitude, get_magnitude(nest(addition(comb[0], comb[1]))))
    max_magnitude = max(max_magnitude, get_magnitude(nest(addition(comb[1], comb[0]))))
print(max_magnitude)

