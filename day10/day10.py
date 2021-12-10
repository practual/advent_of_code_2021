with open('input') as f:
    lines = f.read().split('\n')

bracket_pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>', 
}
bracket_error_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
bracket_correction_points = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}
error_score = 0
correction_scores = []
for line in lines:
    if not line:
        continue
    bracket_stack = []
    for bracket in line:
        if bracket in bracket_pairs.keys():
            bracket_stack.append(bracket)
        else:
            current_open = bracket_stack[-1]
            bracket_stack = bracket_stack[:-1]
            if bracket_pairs[current_open] != bracket:
                error_score += bracket_error_points[bracket]
                break
    else:
        correction_score = 0
        while bracket_stack:
            current_open = bracket_stack[-1]
            bracket_stack = bracket_stack[:-1]
            correction_score = correction_score * 5 + bracket_correction_points[current_open]
        correction_scores.append(correction_score)
            
print(error_score)
correction_scores = sorted(correction_scores)
print(correction_scores[len(correction_scores) // 2])

