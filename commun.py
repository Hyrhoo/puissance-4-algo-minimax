
def is_position_a_winner(board, none_pice, row, col=4, length_win=4):
    item = board[row][col]
    rows = len(board)
    cols = len(board[0])
    if item == none_pice:
        return False
    for delta_row, delta_col in [(1,-1), (0,1), (1,1), (1,0)]:
        consecutive_items = 1
        for delta in (1, -1):
            delta_row *= delta
            delta_col *= delta
            next_row = row + delta_row
            next_col = col + delta_col
            while 0 <= next_row < rows and 0 <= next_col < cols:
                if board[next_row][next_col] == item:
                    consecutive_items += 1
                else:
                    break
                if consecutive_items == length_win:
                    return True
                next_row += delta_row
                next_col += delta_col
    return False

def is_full(board, none_pice=0):
    for row in board:
        for col in row:
            if col == none_pice:
                return False
    return True

def calc_piece_pos(col, board, none_pice=0):
    for row in range(5, -1, -1):
        if board[row][col] == none_pice:
            return (row, col)
    return False
