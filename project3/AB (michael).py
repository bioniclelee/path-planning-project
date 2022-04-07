import sys

queue = {}
empty_board = []
board = []
max_row = 5
max_col = 5
MIN = -10000
MAX = 10000
res_set = set()
overall_lst = []


def is_check(gameboard, pivot_piece):
    res = [False, False]
    for i in gameboard:
        col, row = i
        col = int(ascii_to_index(col))
        row = int(row)
        piece, piece_type = gameboard[i]
        if piece == "King" or piece == "EKing":
            for j in gameboard:
                cur_col, cur_row = j
                cur_col = int(ascii_to_index(cur_col))
                cur_row = int(cur_row)
                cur_piece, cur_piece_type = gameboard[j]
                if cur_piece_type != piece_type:
                    lst = get_threaten_moves(cur_piece, cur_row, cur_col, cur_piece_type, gameboard)
                    for k in lst:
                        if k == (row, col):
                            if piece == "King":
                                res[0] = True
                            else:
                                res[1] = True
        if pivot_piece == "White":
            return res[0]
        return res[1]


def generate_new_gameboard(gameboard, move):
    new_gb = create_gameboard_copy(gameboard)

    temp = new_gb.pop(move[0])
    new_gb[move[1]] = temp
    return new_gb


def all_pieces(gameboard):
    white_pieces = {}
    black_pieces = {}
    for i in gameboard:
        cur_piece, cur_piece_type = gameboard[i]
        if cur_piece_type == "White":
            white_pieces[i] = gameboard[i]
        else:
            black_pieces[i] = gameboard[i]
    return white_pieces, black_pieces


class moves:
    first_move = ""
    gameboard = ""
    lst_gameboard =[]
    count = 1


    def __init__(self, first_move, gameboard):
        self.first_move = first_move
        self.gameboard = gameboard


    def get_row_col_piece_type(self, curr_gameboard, key):
        piece, piece_type = curr_gameboard[key]
        col, row = key
        row = int(row)
        col = int(ascii_to_index(col))
        return row, col, piece, piece_type


    def minimax(self, depth, alpha, beta, turn, curr_gameboard):
        if depth == 0 or is_game_over(curr_gameboard):
            return find_score(curr_gameboard), None

        if turn:
            max_eval = -10000
            best_move = None
            white_pieces = all_pieces(curr_gameboard)[0]
            for white_piece in white_pieces:
                row, col, piece, piece_type = self.get_row_col_piece_type(curr_gameboard, white_piece)
                new_moves = self.generate_next_move(curr_gameboard, white_piece, row, col, piece, piece_type)
                for new_move in new_moves:
                    new_gb = generate_new_gameboard(curr_gameboard, new_move)
                    evaluate, currentmove = self.minimax(depth - 1, alpha, beta, False, new_gb)
                    print("evaluate, currentmove = {}, {}".format(evaluate, currentmove))
                    if evaluate > max_eval:
                        best_move = new_move
                        max_eval = evaluate
                    alpha = max(alpha, evaluate)
                    if beta <= alpha:
                        break
            print("max_eval, best_move = {}, {}".format(max_eval, best_move))
            return max_eval, best_move

        else:
            min_eval = 10000
            best_move = None
            black_pieces = all_pieces(curr_gameboard)[1]
            for black_piece in black_pieces:
                row, col, piece, piece_type = self.get_row_col_piece_type(curr_gameboard, black_piece)
                new_moves = self.generate_next_move(curr_gameboard, black_piece, row, col, piece, piece_type)
                for new_move in new_moves:
                    new_gb = generate_new_gameboard(curr_gameboard, new_move)
                    evaluate, currentmove = self.minimax(depth - 1, alpha, beta, True, new_gb)
                    if evaluate < min_eval:
                        best_move = new_move
                        min_eval = evaluate
                    beta = min(beta, evaluate)
                    if beta <= alpha:
                        break
            return min_eval, best_move


    def generate_next_move(self, curr_gameboard, key, row, col, piece, piece_type):
        lst = []
        threat_moves = get_threaten_moves(piece, row, col, piece_type, curr_gameboard)

        for move in threat_moves:
            temp = create_gameboard_copy(curr_gameboard)
            threaten_row, threaten_col = move
            temp.pop(key)
            temp[index_to_ascii(threaten_col), threaten_row] = (piece, piece_type)
            if not is_check(temp, piece_type):
                lst.append((key, (index_to_ascii(threaten_col), threaten_row)))
        return lst

    def __str__(self):
        return "Gameboard: %s, First move: %s" % (self.gameboard, self.first_move)


def is_game_over(gameboard):
    boo = True
    for i in gameboard:
        col, row = i
        col = int(ascii_to_index(col))
        row = int(row)
        piece, piece_type = gameboard[i]
        if piece == "King" or piece == "EKing":
            all_threats = []
            for j in gameboard:
                cur_col, cur_row = j
                cur_col = int(ascii_to_index(cur_col))
                cur_row = int(cur_row)
                cur_piece, cur_piece_type = gameboard[j]
                if cur_piece_type != piece_type:
                    all_threats.extend(get_threaten_moves(cur_piece, cur_row, cur_col, cur_piece_type, gameboard))
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r <= max_row - 1 and 0 <= c <= max_col - 1 and (r != row or c != col):
                        key = (r, c)
                        if key not in all_threats:
                            boo = False
    return boo


def redo():
    global empty_board
    empty_board = [[0 for i in range(5)] for i in range(5)]


def ascii_to_index(arg):
    return int(ord(arg) - 97)


def index_to_ascii(number):
    return chr(number + 97)


def set_threat_king(row, col, gameboard, piece_type):
    threat_pos = []
    res = 0
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i <= max_row - 1 and 0 <= j <= max_col - 1 and (i != row or j != col):
                key = (index_to_ascii(j), i)
                enemy_piece = ""
                if key in gameboard:
                    enemy_piece = gameboard[key][1]
                if key not in gameboard or enemy_piece != piece_type:
                    if i != row or j != col:
                        threat_pos.append((i, j))
    return threat_pos


def set_threat_queen(row, col, gameboard, piece_type):
    threat1 = set_threat_bishop(row, col, gameboard, piece_type)
    threat1.extend(set_threat_rook(row, col, gameboard, piece_type))
    return threat1


def set_threat_bishop(row, col, gameboard, piece_type):
    count = 1
    threat_pos = []
    while 0 <= row - count < max_row and 0 <= col - count < max_col:
        key = (index_to_ascii(col - count), row - count)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row - count, col - count))
            break
        threat_pos.append((row - count, col - count))
        count += 1

    count = 1
    while 0 <= row + count < max_row and 0 <= col - count < max_col:
        key = (index_to_ascii(col - count), row + count)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row + count, col - count))
            break
        threat_pos.append((row + count, col - count))
        count += 1

    count = 1
    while 0 <= row - count < max_row and 0 <= col + count < max_col:
        key = (index_to_ascii(col + count), row - count)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row - count, col + count))
            break
        threat_pos.append((row - count, col + count))
        count += 1

    count = 1
    while 0 <= row + count < max_row and 0 <= col + count < max_col:
        key = (index_to_ascii(col + count), row + count)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row + count, col + count))
            break
        threat_pos.append((row + count, col + count))
        count += 1

    return threat_pos


def set_threat_rook(row, col, gameboard, piece_type):
    threat_pos = []

    count = 1
    while 0 <= row - count < max_row:
        key = (index_to_ascii(col), row - count)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row - count, col))
            break
        threat_pos.append((row - count, col))
        count += 1

    count = 1
    while 0 <= row + count < max_row:
        key = (index_to_ascii(col), row + count)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row + count, col))
            break
        threat_pos.append((row + count, col))
        count += 1

    count = 1
    while 0 <= col - count < max_col:
        key = (index_to_ascii(col - count), row)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row, col - count))
            break
        threat_pos.append((row, col - count))
        count += 1

    count = 1
    while 0 <= col + count < max_col:
        key = (index_to_ascii(col + count), row)
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                break
            threat_pos.append((row, col + count))
            break
        threat_pos.append((row, col + count))
        count += 1

    return threat_pos


def set_threat_knight(row, col, gameboard, piece_type):
    l = []
    for i in [1, 2]:
        l.append([i, 3 - i])
        l.append([i, -(3 - i)])
        l.append([-i, 3 - i])
        l.append([-i, -(3 - i)])

    threat_pos = []
    for j in l:
        key = (index_to_ascii(col + j[1]), row + j[0])
        if key in gameboard:
            if gameboard[key][1] == piece_type:
                continue
        if 0 <= row + j[0] < max_row and 0 <= col + j[1] < max_col:
            threat_pos.append((row + j[0], col + j[1]))
    return threat_pos


def set_threat_pawn(row, col, gameboard, piece_type):
    threat_pos = []
    if piece_type == "White":
        key = (index_to_ascii(col + 1), row + 1)
        if key in gameboard:
            if gameboard[key][1] != piece_type:
                threat_pos.append((row + 1, col + 1))

        key = (index_to_ascii(col - 1), row + 1)
        if key in gameboard:
            if gameboard[key][1] != piece_type:
                threat_pos.append((row + 1, col - 1))
    else:
        key = (index_to_ascii(col + 1), row - 1)
        if key in gameboard:
            if gameboard[key][1] != piece_type:
                threat_pos.append((row - 1, col + 1))

        key = (index_to_ascii(col - 1), row - 1)
        if key in gameboard:
            if gameboard[key][1] != piece_type:
                threat_pos.append((row - 1, col - 1))

    return threat_pos


def set_non_threat_pawn(row, col, gameboard, piece_type):
    non_threat_pos = []
    key_white = (index_to_ascii(col), row + 1)
    key_black = (index_to_ascii(col), row - 1)
    if piece_type == "White" and key_white not in gameboard:
        if row + 1 < 5:
            non_threat_pos.append((row + 1, col))
    elif piece_type == "Black" and key_black not in gameboard:
        if row - 1 >= 0:
            non_threat_pos.append((row - 1, col))
    return non_threat_pos


def create_board():
    global board
    board = [[0 for i in range(5)] for i in range(5)]
    board[4][4] = "EKing"
    board[4][3] = "EQueen"
    board[4][2] = "EBishop"
    board[4][1] = "EKnight"
    board[4][0] = "ERook"
    board[3][4] = "EPawn"
    board[3][3] = "EPawn"
    board[3][2] = "EPawn"
    board[3][1] = "EPawn"
    board[3][0] = "EPawn"

    board[0][4] = "King"
    board[0][3] = "Queen"
    board[0][2] = "Bishop"
    board[0][1] = "Knight"
    board[0][0] = "Rook"
    board[1][4] = "Pawn"
    board[1][3] = "Pawn"
    board[1][2] = "Pawn"
    board[1][1] = "Pawn"
    board[1][0] = "Pawn"

    for i in range(5):
        for j in range(5):
            if board[i][j] != 0 and board[i][j][0] != "E":
                queue[(index_to_ascii(j), int(i))] = (board[i][j], "White")
            elif board[i][j] != 0:
                queue[(index_to_ascii(j), int(i))] = (board[i][j], "Black")


def get_threaten_moves(piece, row, col, piece_type, gameboard):
    if piece == "King" or piece == "EKing":
        return set_threat_king(row, col, gameboard, piece_type)
    elif piece == "Queen" or piece == "EQueen":
        return set_threat_queen(row, col, gameboard, piece_type)
    elif piece == "Bishop" or piece == "EBishop":
        return set_threat_bishop(row, col, gameboard, piece_type)
    elif piece == "Knight" or piece == "EKnight":
        return set_threat_knight(row, col, gameboard, piece_type)
    elif piece == "Rook" or piece == "ERook":
        return set_threat_rook(row, col, gameboard, piece_type)
    else:
        lst = set_threat_pawn(row, col, gameboard, piece_type)
        lst.extend(set_non_threat_pawn(row, col, gameboard, piece_type))
        return lst


def to_score(piece):
    if piece == "King" or piece == "EKing":
        return 2000
    elif piece == "Queen" or piece == "EQueen":
        return 100
    elif piece == "Bishop" or piece == "EBishop":
        return 30
    elif piece == "Knight" or piece == "EKnight":
        return 30
    elif piece == "Rook" or piece == "ERook":
        return 50
    else:
        return 10


def create_gameboard_copy(gameboard):
    temp = {}
    for i in gameboard:
        temp[i] = gameboard[i]
    return temp


def is_enemy_location(gameboard, row, col, piece_type):
    for i in gameboard:
        gcol, grow = i
        if grow == row and ascii_to_index(gcol) == col:

            gpiece, belongs_to = gameboard[i]
            if belongs_to != piece_type:
                return True
            else:
                return False


def serialize(dct):
    tmp = []
    for i in dct:
        tmp.append((i, dct[i]))
    return tuple(tmp)


def add_to_set(dct):
    global res_set
    # key = list(dct.keys())[0]
    serialized = serialize(dct)
    if serialized not in res_set:
        res_set.add(serialized)
        return True
    return False


def find_score(gameboard):
    own_score = 0
    enemy_score = 0
    for i in gameboard:
        piece, belongs_to = gameboard[i]
        if belongs_to == "White":
            own_score += to_score(piece)
        else:
            enemy_score += to_score(piece)
    return own_score - enemy_score


def studentAgent(gameboard):
    new_move = moves("", gameboard)
    score, first_move = new_move.minimax(3, -10000, 10000, True, new_move.gameboard)
    print(first_move)
    return first_move
    # print(len(all_moves))



if __name__ == "__main__":
    create_board()
    print(studentAgent(queue))
