from collections import defaultdict


with open('input') as f:
    fish = list(map(int, f.readline().strip('\n').split(',')))

fish_states = defaultdict(int)
for f in fish:
    fish_states[f] += 1


def evolve_state(fish_states):
    new_states = {}
    for i in range(8):
        new_states[i] = fish_states[i+1]
    new_states[6] += fish_states[0]
    new_states[8] = fish_states[0]
    return new_states


def count_fish_after_iteration(fish_state, num_days):
    for d in range(num_days):
        fish_state = evolve_state(fish_state)
    return sum(fish_state.values())


print(count_fish_after_iteration(fish_states, 80))
print(count_fish_after_iteration(fish_states, 256))
