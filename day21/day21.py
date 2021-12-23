from collections import defaultdict


with open('input') as f:
    p1_start = int(f.readline().strip('\n').split(' ')[-1]) - 1
    p2_start = int(f.readline().strip('\n').split(' ')[-1]) - 1

p1_pos, p2_pos = p1_start, p2_start
p1_score, p2_score = 0, 0
die_roll = 1
while True:
    p1_roll = die_roll * 3 + 3
    die_roll += 3
    p1_pos = (p1_pos + p1_roll) % 10
    p1_score += p1_pos + 1
    if p1_score >= 1000:
        break
    p2_roll = die_roll * 3 + 3
    die_roll += 3
    p2_pos = (p2_pos + p2_roll) % 10
    p2_score += p2_pos + 1
    if p2_score >= 1000:
        break

print(min(p1_score, p2_score) * (die_roll - 1))


def get_to_21(roll_combinations, rolls, pos, score):
    for roll in range(3, 10):
        new_rolls = rolls[::] + [roll]
        new_pos = (pos + roll) % 10
        new_score = score + new_pos + 1
        if new_score >= 21:
            roll_combinations.append(new_rolls)
        else:
            get_to_21(roll_combinations, new_rolls, new_pos, new_score)


roll_weights = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


def prob_for_rolls(rolls):
    prob = 1
    for roll in rolls:
        prob = prob * roll_weights[roll]
    return prob


def get_move_probs_for_pos(starting_position):
    roll_combinations = []
    get_to_21(roll_combinations, [], starting_position, 0)
    move_probabilities = defaultdict(int)
    for rolls in roll_combinations:
        move_probabilities[len(rolls)] += prob_for_rolls(rolls)
    return move_probabilities


p1_probs = get_move_probs_for_pos(p1_start)
p2_probs = get_move_probs_for_pos(p2_start)


def game_wins(player, moves):
    if player == 1:
        player_probs = p1_probs
        opponent_probs = p2_probs
    else:
        player_probs = p2_probs
        opponent_probs = p1_probs
    if moves not in player_probs:
        return 0
    total_moves = moves * 2 - (1 if player == 1 else 0)
    opponent_moves = total_moves - moves
    removed = 0
    for opponent_win in range(moves - (1 if player == 1 else 0), 0, -1):
        if opponent_win not in opponent_probs:
            continue
        removed += opponent_probs[opponent_win] * 27**(opponent_moves - opponent_win)
    return player_probs[moves] * (27**opponent_moves - removed)


p1_wins = 0
for moves in p1_probs:
    p1_wins += game_wins(1, moves)
p2_wins = 0
for moves in p2_probs:
    p2_wins += game_wins(2, moves)

print(max(p1_wins, p2_wins))

