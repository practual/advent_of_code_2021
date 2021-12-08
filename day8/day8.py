import itertools
import re


with open('input') as f:
    displays = f.read().split('\n')

digit_count = 0
for display in displays:
    if not display:
        continue
    digits = re.match('.*\|(.*)', display)[1].strip().split(' ')
    digit_count += sum(1 for digit in digits if len(digit) in [2, 3, 4, 7])
print(digit_count)

def infer_digits(inputs):
    digits = {}
    fives = []
    sixes = []
    for input in inputs:
        input = set(sorted(input))
        # These digits can be simply idenified by the number of segments.
        if len(input) == 2:
            digits[1] = input
        elif len(input) == 3:
            digits[7] = input
        elif len(input) == 4:
            digits[4] = input
        elif len(input) == 7:
            digits[8] = input
        # We will have three digits for each of 5 and 6 segments.
        elif len(input) == 5:
            fives.append(input)
        elif len(input) == 6:
            sixes.append(input)
    # Get the top segment
    t_s = digits[7] - digits[1]
    # The bottom left and bottom segments
    bl_b_s = digits[8] - digits[4] - t_s
    # The '5-length' digits are 2, 3, 5.
    # '2' - '3' gives the bottom left segment, which we can identify.
    # (The bottom segment will not appear since all share it)
    # But we don't know which are '2' and '3', so loop through each.
    bl_s = None
    for five_pair in itertools.permutations(fives, 2):
        diff = five_pair[0] - five_pair[1]
        if len(diff) == 1 and len(diff - bl_b_s) == 0:
            bl_s = diff
            digits[2] = five_pair[0]
            digits[3] = five_pair[1]
            break
    for five in fives:
        if five != digits[2] and five != digits[3]:
            digits[5] = five
            break
    # Of the '6-length' digits (0, 6, 9), only '9' does not have the
    # bottom left segment
    for six in sixes:
        if len(bl_s - six) == 1:
            digits[9] = six
    for six in sixes:
        if six == digits[9]:
            continue
        if len(digits[4] - digits[1] - six):
            digits[0] = six
        else:
            digits[6] = six
    return {''.join(sorted(segments)): digit for digit, segments in digits.items()}


total_value = 0
for display in displays:
    if not display:
        continue
    match = re.match('(.*)\|(.*)', display)
    analysis = match[1].strip().split(' ')
    output = match[2].strip().split(' ')
    digits = infer_digits(analysis)
    value = ''
    for segments in output:
        value += str(digits[''.join(sorted(segments))]) 
    total_value += int(value)

print(total_value)

