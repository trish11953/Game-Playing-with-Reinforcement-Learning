# Author: Trisha Mandal
from copy import deepcopy
import os

# used starter code provided to us (host.py)


if os.path.isfile("output.txt"):
    os.remove("output.txt")
boardsize, previousb, currentb, maxint = 5, [], [], float('inf')
f = open('input.txt', 'r')
lines = f.read().split('\n')
previousb = [[int(x) for x in line.rstrip('\n')] for line in lines[1:6]]
currentb = [[int(x) for x in line.rstrip('\n')] for line in lines[6:11]]
depth, piecetype, blackstones, whitestones = 4, int(lines[0]), 0, 0


def detect_neighbor(i, j):  # host.py
    board, neighbors = currentb, []
    if i > 0:
        neighbors.append((i - 1, j))
    if i < len(board) - 1:
        neighbors.append((i + 1, j))
    if j > 0:
        neighbors.append((i, j - 1))
    if j < len(board) - 1:
        neighbors.append((i, j + 1))
    return neighbors


def detect_neighbor_ally(i, j, board, piecetype):  # host.py
    neighbors, group_allies = detect_neighbor(i, j), []
    for ne in neighbors:
        if board[ne[0]][ne[1]] == piecetype:
            group_allies.append(ne)
    return group_allies


def all_positions(i, j, board, piecetype):  # host.py
    stack, ally_members = [(i, j)], []
    while stack:
        piece = stack.pop()
        ally_members.append(piece)
        neighbor_allies = detect_neighbor_ally(piece[0], piece[1], board, piecetype)
        for ally in neighbor_allies:
            if ally not in stack and ally not in ally_members:
                stack.append(ally)
    return ally_members


def find_count_liberty(i, j, board, piecetype):  # host.py
    my_all_allies = all_positions(i, j, board, piecetype)
    for ally in my_all_allies:
        neighbors = detect_neighbor(ally[0], ally[1])
        for piece in neighbors:
            if board[piece[0]][piece[1]] == 0:
                return True
    return False


def find_died_pieces(piecetype, board):  # host.py
    boardsize, died_pieces = 5, []
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if board[i][j] == piecetype:
                if not find_count_liberty(i, j, board, piecetype):
                    died_pieces.append((i, j))
    return died_pieces


def get_liberty_positions(i, j, board, piecetype):
    chain, liberties = all_positions(i, j, board, piecetype), set()
    for p in chain:
        neighbors = detect_neighbor(p[0], p[1])
        for piece in neighbors:
            b = board[piece[0]][piece[1]]
            if b == 0:
                liberties |= {piece}
    lst = list(liberties)
    return lst


def getneighborlibertypos(i, j, board, piecetype):
    neighbors, liberties = detect_neighbor(i, j), set()
    for piece in neighbors:
        b = board[piece[0]][piece[1]]
        if b == 0:
            liberties |= {piece}
    lst = list(liberties)
    return lst


def try_move(i, j, board, piecetype):
    new_board = board

    new_board[i][j] = piecetype
    died_pieces = find_died_pieces(3 - piecetype, new_board)
    deadp = len(died_pieces)
    if deadp == 0:
        return new_board, len(died_pieces), new_board
    else:
        for piece in died_pieces:
            new_board[piece[0]][piece[1]] = 0
        next_board = new_board
        return next_board, deadp, new_board


def valid_moves(piecetype, previous_board, new_board):
    boardsize, moves, imp_moves, counter, trial, self_end_1, safe_moves_important, alllibertiesmv = 5, [], [], 1, 0, [], [], set()

    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if new_board[i][j] == piecetype:
                self_end = get_liberty_positions(i, j, new_board, piecetype)
                if len(self_end) == 1:
                    alllibertiesmv |= set(self_end)
                    if i == 0 or i == 4 or j == 0 or j == 4:
                        safe = getneighborlibertypos(self_end[0][0], self_end[0][1], new_board, piecetype)
                        if safe:
                            alllibertiesmv |= set(safe)
            elif new_board[i][j] == 3 - piecetype:
                oppo_end = get_liberty_positions(i, j, new_board, 3 - piecetype)
                alllibertiesmv |= set(oppo_end)
    x = len(list(alllibertiesmv))
    if x:
        lst = list(alllibertiesmv)
        for x in lst:
            board_after_move, died_pieces, _ = try_move(x[0], x[1], deepcopy(new_board), piecetype)
            if find_count_liberty(x[0], x[1], board_after_move,
                                  piecetype):
                if board_after_move != new_board:
                    if board_after_move != previous_board:
                        imp_moves.append((x[0], x[1], died_pieces))
        if len(imp_moves) > 0:
            sor = sorted(imp_moves, key=lambda x: x[2], reverse=True)
            return sor

    for i in range(0, boardsize):
        for j in range(0, boardsize):
            n = new_board[i][j]
            if n == 0:
                board_after_move, died_pieces, notimp = try_move(i, j, deepcopy(new_board), piecetype)
                if find_count_liberty(i, j, board_after_move,
                                      piecetype):
                    if board_after_move != new_board:
                        if board_after_move != previous_board:
                            moves.append((i, j, died_pieces))

    arranged = sorted(moves, key=lambda x: x[2], reverse=True)
    return arranged


def evaluation_function(board, piecetype, died_pieces_black, died_pieces_white):
    boardsize, blackpieces, whitepieces, blackdanger, whitedanger = 5, 0, 0, 0, 0
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            b = board[i][j]
            if b == 1:
                lib = get_liberty_positions(i, j, board, 1)
                if len(lib) <= 1:
                    blackdanger += 1
                blackpieces += 1
            if b == 2:
                lib = get_liberty_positions(i, j, board, 2)
                if len(lib) <= 1:
                    whitedanger += 1
                whitepieces += 1
    if piecetype == 1:
        p1 = 10 * blackpieces - 10 * whitepieces
        p2 = 2 * whitedanger - 1.5 * blackdanger
        eval_value = p1 + p2
    else:
        p1 = - 10 * blackpieces + 10 * whitepieces
        p2 = - 1.5 * whitedanger + 2 * blackdanger
        eval_value = p1 + p2
    return eval_value


def maximize(board, previous_board, piecetype, depth, alpha, beta, newboardnodead):
    global blackstones
    global whitestones
    dead = len(find_died_pieces(piecetype, newboardnodead))
    if piecetype == 1:
        died_pieces_black = dead
        blackstones += died_pieces_black
    if piecetype == 2:
        died_pieces_white = dead
        whitestones += died_pieces_white

    if depth == 0:
        value = evaluation_function(board, piecetype, blackstones, whitestones)
        if piecetype == 1:
            leng = len(find_died_pieces(1, newboardnodead))
            blackstones = blackstones - leng
        if piecetype == 2:
            leng = len(find_died_pieces(2, newboardnodead))
            whitestones = whitestones - leng
        return value, []

    scoremax, maxactions, memoves = float("-inf"), [], valid_moves(piecetype, previous_board, board)
    if len(memoves) == 25:
        return 100, [(2, 2)]
    for move in memoves:
        next_board, died_pieces, newboardnodead = try_move(move[0], move[1], deepcopy(board), piecetype)
        score, actions = minimize(next_board, board, 3 - piecetype, depth - 1, alpha, beta,
                                  newboardnodead)
        if scoremax > beta:
            return scoremax, maxactions
        if score > scoremax:
            scoremax, maxactions = score, [move] + actions
        if scoremax > alpha:
            alpha = scoremax
    return scoremax, maxactions


def minimize(board, previous_board, piecetype, depth, alpha, beta, newboardnodead):
    global blackstones
    global whitestones
    dead = len(find_died_pieces(piecetype, newboardnodead))
    if piecetype == 1:
        died_pieces_black = dead
        blackstones = blackstones + died_pieces_black
    if piecetype == 2:
        died_pieces_white = dead
        whitestones = whitestones + died_pieces_white

    if depth == 0:
        value = evaluation_function(board, piecetype, blackstones, whitestones)
        if piecetype == 1:
            leng = len(find_died_pieces(1, newboardnodead))
            blackstones = blackstones - leng
        if piecetype == 2:
            leng = len(find_died_pieces(2, newboardnodead))
            whitestones = whitestones - leng
        return value, []

    scoremin, minactions, memoves = float("inf"), [], valid_moves(piecetype, previous_board, board)

    for move in memoves:
        next_board, died_pieces, newboardnodead = try_move(move[0], move[1], deepcopy(board), piecetype)
        score, actions = maximize(next_board, board, 3 - piecetype, depth - 1, alpha, beta,
                                  newboardnodead)
        if scoremin < alpha:
            return scoremin, minactions
        if score < scoremin:
            scoremin, minactions = score, [move] + actions
        if scoremin < beta:
            alpha = scoremin
    return scoremin, minactions


score, actions = maximize(currentb, previousb, piecetype, depth, -maxint, maxint, currentb)
if len(actions) > 0:
    action = actions[0]
else:
    action = "PASS"

if action == "PASS":
    f = open("output.txt", "w")
    f.write("PASS")
else:
    f = open("output.txt", "w")
    f.write(str(action[0]))
    f.write(',')
    f.write(str(action[1]))
