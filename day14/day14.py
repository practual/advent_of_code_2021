from collections import defaultdict


rule_map = {}

with open('input') as f:
    polymer = f.readline().strip('\n')
    for rule in f.read().split('\n'):
        if not rule:
            continue
        pair, _, insert = rule.split(' ')
        rule_map[tuple(pair)] = ((pair[0], insert), (insert, pair[1]))

pair_count = defaultdict(int)
for i in range(len(polymer) - 1):
    pair_count[(polymer[i], polymer[i+1])] += 1


def iterate_pairs(pair_count):
    new_pair_count = defaultdict(int)
    for pair, count in pair_count.items():
        new_pairs = rule_map[pair]
        new_pair_count[new_pairs[0]] += count
        new_pair_count[new_pairs[1]] += count
    return new_pair_count


def count_letters(pair_count):
    letter_count = defaultdict(int)
    for pair, count in pair_count.items():
        letter_count[pair[0]] += count
        letter_count[pair[1]] += count
    letter_count[polymer[0]] += 1
    letter_count[polymer[-1]] += 1

    min_letter = None
    max_letter = 0
    for count in letter_count.values():
        min_letter = count if not min_letter else min(min_letter, count)
        max_letter = max(max_letter, count)
    return (max_letter - min_letter) // 2

pair_count_copy = pair_count.copy()
for i in range(10):
    pair_count = iterate_pairs(pair_count)
print(count_letters(pair_count))

pair_count = pair_count_copy
for i in range(40):
    pair_count = iterate_pairs(pair_count)
print(count_letters(pair_count))

