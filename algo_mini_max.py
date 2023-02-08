
from commun import is_position_a_winner, calc_piece_pos, is_full

def inverse(pice):
    if pice == 1: return 2
    if pice == 2: return 1

def mid(a,b):
    a1 = abs(a-3)
    b1 = abs(b-3)
    if a1 < b1:
        return a
    else:
        return b

def get_hash(board):
    return hash(tuple([tuple(i) for i in board]))

def load_save(board):
    try:
        return save[get_hash(board)]
    except KeyError:
        return None

def save_calcul(board, score):
    global save
    try:
        save[get_hash(board)] = score
    except KeyError:
        pass

test = [3,2,4,1,5,0,6]
def ia(board, pice, turn, limit=6):
    global save
    save = {}
    best_score = -100
    move = None
    for i in range(7):
        col = test[i]
        pos = calc_piece_pos(col, board)
        if pos:
            board[pos[0]][pos[1]] = pice
            score = mini_max_min(board, inverse(pice), limit-1, pos, -50, 50, turn)
            board[pos[0]][pos[1]] = 0
            print(best_score, score, move, col)
            if score > best_score:
                best_score, move = score, col
            elif score == best_score:
                move = mid(move, col)
    return move

def mini_max_max(board, pice, limit, last_move, alpha, beta, turn):
    global save
    load = load_save(board)
    if load is not None:
        return load
    if is_position_a_winner(board, 0, last_move[0], last_move[1]):
        score = -22
        save_calcul(board, score)
        return score
    elif limit == 0 or turn == 42:
        save_calcul(board, 0)
        return 0
    else:
        turn += 1
        best_score = -50
        for i in range(7):
            col = test[i]
            pos = calc_piece_pos(col, board)
            if pos:
                board[pos[0]][pos[1]] = pice
                score = mini_max_min(board, inverse(pice), limit-1, pos, alpha, beta, turn)
                if score != 0:
                    score -= (1 if score > 0 else -1)
                board[pos[0]][pos[1]] = 0
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        save_calcul(board, best_score)
        return best_score

def mini_max_min(board, pice, limit, last_move, alpha, beta, turn):
    global save
    load = load_save(board)
    if load is not None:
        return load
    if is_position_a_winner(board, 0, last_move[0], last_move[1]):
        score = 22
        save_calcul(board, score)
        return score
    elif limit == 0 or turn == 42:
        save_calcul(board, 0)
        return 0
    else:
        turn += 1
        best_score = 50
        for i in range(7):
            col = test[i]
            pos = calc_piece_pos(col, board)
            if pos:
                board[pos[0]][pos[1]] = pice
                score = mini_max_max(board, inverse(pice), limit-1, pos, alpha, beta, turn)
                board[pos[0]][pos[1]] = 0
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        save_calcul(board, best_score)
        return best_score

if __name__ == "__main__":
    import time
    turn = 15
    board = [
        [0,0,0,2,1,0,0],
        [0,0,0,1,2,0,0],
        [0,0,0,2,1,0,0],
        [0,0,0,1,2,0,0],
        [0,0,0,2,1,0,0],
        [0,0,2,1,1,2,0]
    ]
    #turn = 1
    #board = [[0 for _ in range(7)] for _ in range(6)]
    t=time.monotonic()
    print(ia(board, 1, turn, 16))
    print(time.monotonic()-t)