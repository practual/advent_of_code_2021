from collections import defaultdict


with open('input') as f:
    numbers = map(int, f.readline().strip('\n').split(','))

    boards = []
    board = [[]]
    board_num = 0
    board_row = 0
    number_map = defaultdict(list)
    board_hits = []
    while True:
        row = f.readline()
        if not row:
            break
        row = row.strip('\n')
        if not row:
            continue
        row = map(int, row.split())
        for number in row:
            number_map[number].append(board_num)
            board[board_row].append(number)
        board_row += 1
        if board_row == 5:
            boards.append(board)
            board_hits.append(defaultdict(int))
            board_row = 0
            board_num += 1
            board = [[]]
        else:
            board.append([])

def find_in_board(board, number):
    for i in range(5):
        for j in range(5):
            if board[i][j] == number:
                return i, j


def check_row(board_hits, row):
    for j in range(5):
        if not board_hits[(row, j)]:
            return False
    return True


def check_col(board_hits, col):
    for i in range(5):
        if not board_hits[(i, col)]:
            return False
    return True
 

def sum_board(board):
    return sum(sum(board_row) for board_row in board)


def sum_of_numbers_in_board(board_num, numbers):
    number_sum = 0
    for number in numbers:
        if board_num in number_map[number]:
            number_sum += number
    return number_sum 


seen_numbers = []
has_bingos = set()
for number in numbers:
    seen_numbers.append(number)
    for board_with_number in number_map[number]:
        coords = find_in_board(boards[board_with_number], number)
        board_hits[board_with_number][coords] = 1
        if check_row(board_hits[board_with_number], coords[0]) or check_col(board_hits[board_with_number], coords[1]):
            remaining = sum_board(boards[board_with_number]) - sum_of_numbers_in_board(board_with_number, seen_numbers)
            if board_with_number not in has_bingos:
                has_bingos.add(board_with_number)
                if len(has_bingos) == 1 or len(has_bingos) == len(boards):
                    print(remaining * number)
            
