from copy import deepcopy
import os

blackstones, whitestones, boardsize = 0, 0, 5

if os.path.isfile("output.txt"):
    os.remove("output.txt")
boardsize, previousb, currentb, maxint = 5, [], [], float('inf')
f = open('input.txt', 'r')
lines = f.read().split('\n')
for line in lines[1:6]:
    for i in line.rstrip('\n'):
        previousb.append(int(i))
currentb = [[int(x) for x in line.rstrip('\n')] for line in lines[6:11]]
depth, piecetype = 4, int(lines[0])


def on_board(i, j):
    if 5 > i >= 0 and 5 > j >= 0:
        return True
    else:
        return False


# def detect_neighbor(i, j):
#     neighbors = []
#     coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]
#     for co in coordinates:
#         new_x = i + co[0]
#         new_y = j + co[1]
#         if on_board(new_x, new_y):
#             neighbors.append((new_x, new_y))
#     return neighbors

def getneighbors(i, j):  # done
    box, neighbors = [], []
    box.append((0, -1))
    box.append((0, 1))
    box.append((1, 0))
    box.append((-1, 0))
    for c in box:
        if 0 <= j + c[1] < boardsize:
            if 0 <= i + c[0] < boardsize:
                neighbors.append((i + c[0], j + c[1]))
    return neighbors


def detect_neighbor_ally(i, j, board, player):
    neighbors = getneighbors(i, j)  # Detect neighbors
    group_allies = []
    for ne in neighbors:
        # the same color
        if board[ne[0]][ne[1]] == player:
            group_allies.append(ne)
    return group_allies


def all_ally_positions(i, j, board, player):
    # https://github.com/umbriel47/aigo/blob/master/board.py#L95

    if not on_board(i, j):
        return []

    all_allies = []
    neighbors = detect_neighbor_ally(i, j, board, player)
    all_allies.append((i, j))
    visited = {}
    visited[(i, j)] = True
    while True:
        temp_list = neighbors
        neighbors = []
        for x, y in temp_list:
            if (x, y) not in visited and board[x][y] == player:
                all_allies.append((x, y))
                visited[(x, y)] = True
                next_neighbor = detect_neighbor_ally(x, y, board, player)
                for ne in next_neighbor:
                    neighbors.append(ne)
        if len(neighbors) == 0:
            return []
    return all_allies


# def all_positions(i, j, board, player):
#     stack = [(i, j)]  # stack for DFS serach
#     ally_members = []  # record allies positions during the search
#     while stack:
#         piece = stack.pop()
#         ally_members.append(piece)
#         neighbor_allies = detect_neighbor_ally(piece[0], piece[1], board, player)
#         for ally in neighbor_allies:
#             if ally not in stack and ally not in ally_members:
#                 stack.append(ally)
#     return ally_members

def chains(i, j, board, piecetype):  # done
    vis, stack, chain = {}, [(i, j)], []
    vis[(i, j)] = True
    while stack:
        cur = stack.pop()
        chain.append(cur)
        for n in getneighbors(cur[0], cur[1]):
            if board[n[0]][n[1]] == piecetype and n not in vis:
                stack.append(n)
                vis[n] = True
    return chain


# def find_count_liberty(i, j, board, player):
#     my_all_allies = all_positions(i, j, board, player)
#     # print("hey in function fcl",my_all_allies)
#     for ally in my_all_allies:
#         neighbors = detect_neighbor(ally[0], ally[1])
#         # print("kiii",neighbors)
#         for piece in neighbors:
#             # print("piece",piece)
#             if board[piece[0]][piece[1]] == 0:
#                 return True
#     return False
def findliberties(i, j, board, piecetype):  # done
    c, liberties = chains(i, j, board, piecetype), set()
    for piece in c:
        nei = getneighbors(piece[0], piece[1])
        for n in nei:
            b = board[n[0]][n[1]]
            if b == 0:
                return True
    return False


def finddeadpieces(player, board):
    dead = []
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if board[i][j] == player and not findliberties(i, j, board, player):
                dead.append((i, j))
    return dead


# check for capture liberty....
# check for self capture
# def getlibertypos(i, j, board, player):
#     liberties = set()
#     allyMembers = chains(i, j, board, player)
#     for member in allyMembers:
#         neighbors = getneighbors(member[0], member[1])
#         for piece in neighbors:
#             if board[piece[0]][piece[1]] == 0:
#                 liberties = liberties | {piece}
#     return list(liberties)

def getlibertypos(i, j, board, piecetype):  # done
    c, liberties = chains(i, j, board, piecetype), set()
    for piece in c:
        nei = getneighbors(piece[0], piece[1])
        for n in nei:
            b = board[n[0]][n[1]]
            if b == 0:
                liberties.add(n)
    return list(liberties)


def libertyposforneighbor(i, j, board, player):
    nei, liberties = getneighbors(i, j), set()
    for piece in nei:
        b = board[piece[0]][piece[1]]
        if b == 0:
            liberties.add(piece)
    return list(liberties)


def try_move(i, j, board, piecetype):
    new_board = board
    new_board[i][j] = piecetype
    dead = finddeadpieces(3 - piecetype, new_board)

    if len(dead) == 0:
        return new_board, len(dead), new_board
    else:
        cp = deepcopy(new_board)
        for piece in dead:
            cp[piece[0]][piece[1]] = 0
        next_board = cp

        return next_board, len(dead), new_board


def valid_moves(player, previous_board, new_board):
    moves, imp_moves, counter, trial, self_end_1, safe_moves_important, self_end_2, oppo_end_2, all_liberties_vala_move  = [], [], 1, 0, [], [], set(), set(), set()
    for i in range(0, 5):
        for j in range(0, 5):
            # print(player)
            if new_board[i][j] == player:
                # print(i,j)
                self_end = getlibertypos(i, j, new_board, player)
                # print("yahi hai khatarnak",self_end)
                if len(self_end) == 1:
                    all_liberties_vala_move = all_liberties_vala_move | set(self_end)
                    if i == 0 or i == 4 or j == 0 or j == 4:
                        safe_positions = libertyposforneighbor(self_end[0][0], self_end[0][1], new_board, player)
                        if safe_positions:
                            all_liberties_vala_move = all_liberties_vala_move | set(safe_positions)
                        # all_liberties_vala_move.add(set(safe_positions))
                    # print("kaise",all_liberties_vala_move_1)
                    # return list(all_liberties_vala_move_1)

            elif new_board[i][j] == 3 - player:
                oppo_end = getlibertypos(i, j, new_board, 3 - player)
                # print("oopo",i,j,oppo_end)
                all_liberties_vala_move = all_liberties_vala_move | set(oppo_end)

    if len(list(all_liberties_vala_move)):
        # print("yaar")
        for x in list(all_liberties_vala_move):
            tri_board = deepcopy(new_board)
            board_after_move, died_pieces, _ = try_move(x[0], x[1], tri_board, player)
            # print(x[0],x[1],died_pieces)
            # print("condition 4",find_count_liberty(i, j, board_after_move, player))
            if findliberties(x[0], x[1], board_after_move,
                             player) and board_after_move != new_board and board_after_move != previous_board:
                imp_moves.append((x[0], x[1], died_pieces))
        if len(imp_moves) != 0:
            return sorted(imp_moves, key=lambda x: x[2], reverse=True)

    for i in range(0, boardsize):
        for j in range(0, boardsize):

            if new_board[i][j] == 0:

                trial_board = deepcopy(new_board)
                board_after_move, died_pieces, _ = try_move(i, j, trial_board, player)
                # print("condition 4",find_count_liberty(i, j, board_after_move, player))
                if findliberties(i, j, board_after_move,
                                 player) and board_after_move != new_board and board_after_move != previous_board:
                    # print("check in vm",endangeredLiberties(board_after_move,player))

                    # print("idhar")
                    moves.append((i, j, died_pieces))

    return sorted(moves, key=lambda x: x[2], reverse=True)

    # improvise


def get_group_count_with_k_liberties(board, player, k):
    mine_grps_count = 0
    opponent_gps_count = 0

    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == player:
                lib = getlibertypos(i, j, board, player)
                if len(set(lib)) <= k:
                    mine_grps_count = mine_grps_count + len(lib)
            if board[i][j] == 3 - player:
                lib = getlibertypos(i, j, board, 3 - player)
                if len(set(lib)) <= k:
                    opponent_gps_count = opponent_gps_count + len(lib)

    return mine_grps_count, opponent_gps_count


def evaluation_function(board, player, died_pieces_black, died_pieces_white):
    black_count = 0
    white_count = 0
    black_endangered_liberty = 0
    white_endangered_liberty = 0
    white_total_liberty = set()
    black_total_liberty = set()
    # self_groups,oppo_groups=get_group_count_with_k_liberties(board,player,2)
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == 1:
                lib = getlibertypos(i, j, board, 1)
                # black_total_liberty=black_total_liberty | set(lib)
                if len(lib) <= 1:  # try 2
                    black_endangered_liberty = black_endangered_liberty + 1
                black_count += 1
            elif board[i][j] == 2:
                lib = getlibertypos(i, j, board, 2)
                # white_total_liberty=white_total_liberty | set(lib)
                if len(lib) <= 1:
                    white_endangered_liberty = white_endangered_liberty + 1
                white_count += 1
    white_count = white_count + 2.5
    if player == 1:
        eval_value = black_count - white_count + white_endangered_liberty - black_endangered_liberty + died_pieces_white * 10 - died_pieces_black * 16  # try my total-uska total liberty
    else:
        eval_value = -black_count + white_count - white_endangered_liberty + black_endangered_liberty + died_pieces_black * 10 - died_pieces_white * 16

    # eval_value=eval_value+oppo_groups-self_groups
    # print("player",player,eval_value)
    return eval_value


def best_move(board, previous_board, player, depth):
    died_pieces_white = 0
    score, actions = maximizer_value(board, previous_board, player, depth, float("-inf"), float("inf"), board)
    # print("yaar",score,actions)
    if len(actions) > 0:
        return actions[0]
    else:
        return "PASS"


def maximizer_value(board, previous_board, player, depth, alpha, beta, new_board_without_died_pieces):
    global blackstones
    global whitestones
    if player == 2:
        died_pieces_white = len(finddeadpieces(player, new_board_without_died_pieces))
        whitestones = whitestones + died_pieces_white
    if player == 1:
        died_pieces_black = len(finddeadpieces(player, new_board_without_died_pieces))
        blackstones = blackstones + died_pieces_black

    if depth == 0:
        value = evaluation_function(board, player, blackstones, whitestones)
        if player == 1:
            blackstones = blackstones - len(finddeadpieces(1, new_board_without_died_pieces))
        if player == 2:
            whitestones = whitestones - len(finddeadpieces(2, new_board_without_died_pieces))
        return value, []

    max_score = float("-inf")
    max_score_actions = []
    my_moves = valid_moves(player, previous_board, board)
    # print(type(my_moves))
    # print(len(my_moves))
    if len(my_moves) == 25:
        return 100, [(2, 2)]
    for move in my_moves:
        # print("idhar",move[0],move[1])
        trial_board = deepcopy(board)
        next_board, died_pieces, new_board_without_died_pieces = try_move(move[0], move[1], trial_board, player)
        # print("move max",move,died_pieces)
        score, actions = minimizer_value(next_board, board, 3 - player, depth - 1, alpha, beta,
                                         new_board_without_died_pieces)

        if score > max_score:
            max_score = score
            max_score_actions = [move] + actions

        if max_score > beta:
            return max_score, max_score_actions

        if max_score > alpha:
            alpha = max_score

    return max_score, max_score_actions


def minimizer_value(board, previous_board, player, depth, alpha, beta, new_board_without_died_pieces):
    global blackstones
    global whitestones
    if player == 2:
        died_pieces_white = len(finddeadpieces(player, new_board_without_died_pieces))
        whitestones = whitestones + died_pieces_white
    if player == 1:
        died_pieces_black = len(finddeadpieces(player, new_board_without_died_pieces))
        blackstones = blackstones + died_pieces_black

    if depth == 0:
        value = evaluation_function(board, player, blackstones, whitestones)
        if player == 1:
            blackstones = blackstones - len(finddeadpieces(1, new_board_without_died_pieces))
        if player == 2:
            whitestones = whitestones - len(finddeadpieces(2, new_board_without_died_pieces))
        return value, []

    min_score = float("inf")
    min_score_actions = []
    my_moves = valid_moves(player, previous_board, board)

    for move in my_moves:
        trial_board = deepcopy(board)
        next_board, died_pieces, new_board_without_died_pieces = try_move(move[0], move[1], trial_board, player)
        # print("move min",move,died_pieces)
        score, actions = maximizer_value(next_board, board, 3 - player, depth - 1, alpha, beta,
                                         new_board_without_died_pieces)
        # print("min",score,actions)

        if score < min_score:
            min_score = score
            min_score_actions = [move] + actions

        if min_score < alpha:
            return min_score, min_score_actions

        if min_score < beta:
            alpha = min_score

    return min_score, min_score_actions


good_move = best_move(currentb, previousb, piecetype, depth)
action = ""
if good_move == "PASS":
    f = open("output.txt", "w")
    f.write("PASS")
else:
    f = open("output.txt", "w")
    f.write(str(good_move[0]))
    f.write(',')
    f.write(str(good_move[1]))



# def neighbor(i, j):
#     neighbors = []
#     coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]
#     neighbors = [(i+c[0],j+c[1]) for c in coordinates if (0<=j+c[1]<5 and 0<=i+c[0]<5)]
#     return neighbors
#
# def copy(board):  # done
#     new_board = []
#     for i in range(boardsize):
#         new_board.append([])
#     for i in range(boardsize):
#         for j in range(boardsize):
#             new_board[i].append(board[i][j])
#     return new_board
#
#
# def chains(i, j, board, piecetype):
#     vis, stack, chain = {}, [(i, j)], []
#     vis[(i, j)] = True
#     while stack:
#         cur = stack.pop()
#         chain.append(cur)
#         for n in neighbor(cur[0], cur[1]):
#             if board[n[0]][n[1]] == piecetype and n not in vis:
#                 stack.append(n)
#                 vis[n] = True
#     return chain
#
#
# def dead_pieces(piecetype, board):  # done
#     dead, lib = [], False
#     for a in range(0, boardsize):
#         for b in range(0, boardsize):
#             if piecetype == board[a][b]:
#                 c = chains(a, b, board, piecetype)
#                 for piece in c:
#                     n = neighbor(piece[0], piece[1])
#                     for nei in n:
#                         b = board[nei[0]][nei[1]]
#                         if b == 0:
#                             lib = True
#                 if not lib:
#                     dead.append((a, b))
#     return dead
#
#
# def positionofliberty(i, j, board, piecetype):  # done
#     c, liberties = chains(i, j, board, piecetype), set()
#     for piece in c:
#         nei = neighbor(piece[0], piece[1])
#         for n in nei:
#             b = board[n[0]][n[1]]
#             if b == 0:
#                 liberties.add(n)
#     return liberties
#
#
# def evaluation(board, piecetype):  # done
#     whitepieces, whitedanger, blackpieces, blackdanger = 6, 0, 0, 0
#     for i in range(0, boardsize):
#         for j in range(0, boardsize):
#             if board[i][j] == 2:
#                 lib_count = len(positionofliberty(i, j, board, 2))
#                 if lib_count <= 1:
#                     whitedanger += 1
#                 whitepieces += 1
#             elif board[i][j] == 1:
#                 lib_count = len(positionofliberty(i, j, board, 1))
#                 if lib_count <= 1:
#                     blackdanger += 1
#                 blackpieces += 1
#     if piecetype == 1:
#         p1 = (10 * blackpieces) - (10 * whitepieces)
#         p2 = (2 * whitedanger) - ((3 / 2) * blackdanger)
#         eval = p1 + p2
#     elif piecetype == 2:
#         p1 = (10 * whitepieces) - (10 * blackpieces)
#         p2 = (2 * blackdanger) - ((3 / 2) * whitedanger)
#         eval = p1 + p2
#     return eval
#
#
# def bestmoves(piecetype, prev_board, cur_board):
#     best, all_moves = [], set()
#     for i in range(0, boardsize):
#         for j in range(0, boardsize):
#             if cur_board[i][j] != 0:
#                 all_moves |= positionofliberty(i, j, cur_board, cur_board[i][j])
#     for pos in all_moves:
#         cp = copy(cur_board)
#         cp[pos[0]][pos[1]] = piecetype
#         cenemy, cmy = 0, 0
#         enemydead, mydead = dead_pieces(3 - piecetype, cp), dead_pieces(piecetype, cp)
#         for piece in enemydead:
#             cenemy += 1
#             cp[piece[0]][piece[1]] = 0
#         for piece in mydead:
#             cmy += 1
#             cp[piece[0]][piece[1]] = 0
#
#         board_after_move, numofmydeadpieces, numofenemydeadpieces = cp, cmy, cenemy
#         if board_after_move != cur_board:
#             if board_after_move != prev_board:
#                 best.append((pos, numofenemydeadpieces - numofmydeadpieces))
#
#     best = sorted(best, key=lambda x: -x[1])
#     valid_moves = []
#     for i in best:
#         valid_moves.append(i[0])
#
#     return valid_moves
#
#
# def maximize(currentb, previousb, piecetype, depth, alpha, beta):
#     enemypieces = mypieces = 0
#     if depth == 0:
#         return evaluation(currentb, piecetype), []
#     # Counting player and opponent pieces
#     for i in range(boardsize):
#         for j in range(boardsize):
#             if currentb[i][j] == 3 - piecetype:
#                 enemypieces = enemypieces + 1
#             if currentb[i][j] == piecetype:
#                 mypieces = mypieces + 1
#
#         if piecetype == 1:
#             my_count = enemypieces
#             opp_count = mypieces
#         elif piecetype == 2:
#             my_count = mypieces
#             opp_count = enemypieces
#
#     if opp_count == my_count == 0:
#         return 100, [(2, 2)]
#
#     if my_count == 0:
#         if opp_count == 1:
#             if currentb[2][2] == 3 - piecetype:
#                 return 100, [(2, 1)]
#             else:
#                 return 100, [(2, 2)]
#     mymoves = bestmoves(piecetype, previousb, currentb)
#     max = -maxint
#     maxaction = []
#     for move in mymoves:
#         '''
#         1. score for each move
#         2. getting the min of all scores
#         3. prune
#         '''
#         cp = copy(currentb) # copy board
#         cp[move[0]][move[1]] = piecetype # place  move
#         enemydead, mydead = dead_pieces(3 - piecetype, cp), dead_pieces(piecetype, cp) # dead pieces
#
#         for piece in enemydead:
#             cp[piece[0]][piece[1]] = 0
#         for piece in mydead:
#             cp[piece[0]][piece[1]] = 0
#         next_board, numofmydeadpieces, numofenemydeadpieces = cp, len(mydead), len(enemydead)
#
#
#         value, actions = minimize(next_board, currentb, 3 - piecetype, depth - 1, alpha, beta)
#         value += (numofenemydeadpieces * 5)
#         value -= (numofmydeadpieces * (17/2))
#
#         if value > max:
#             max, maxaction = value, [move] + actions
#
#         if max >= beta:
#             return max, maxaction
#
#         if max > alpha:
#             alpha = max
#
#     return max, maxaction
#
#
# def minimize(cur_board, prev_board, piecetype, depth, alpha, beta):
#     enemypieces = mypieces = 0
#     min = maxint
#
#     if depth == 0:
#         return evaluation(cur_board, piecetype), []
#
#     for i in range(boardsize):
#         for j in range(boardsize):
#             if cur_board[i][j] == 3 - piecetype:
#                 enemypieces += 1
#             if cur_board[i][j] == piecetype:
#                 mypieces += 1
#
#     if piecetype == 1:
#         my_count = enemypieces
#         opp_count = mypieces
#     elif piecetype == 2:
#         my_count = mypieces
#         opp_count = enemypieces
#
#     if my_count == opp_count == 0:
#         return 100, [(2, 2)]
#     if my_count == 0:
#         if opp_count == 1:
#             if cur_board[2][2] == 3 - piecetype:
#                 return 100, [(2, 1)]
#             else:
#                 return 100, [(2, 2)]
#
#     my_moves = bestmoves(piecetype, prev_board, cur_board)
#
#     minaction = []
#     for move in my_moves:
#         cp = copy(cur_board)
#         cp[move[0]][move[1]] = piecetype
#         enemydead, mydead = dead_pieces(3 - piecetype, cp), dead_pieces(piecetype, cp)
#         for piece in enemydead:
#             cp[piece[0]][piece[1]] = 0
#         for piece in mydead:
#             cp[piece[0]][piece[1]] = 0
#
#
#         next_board, numofmydeadpieces, numofenemydeadpieces = cp, len(mydead), len(enemydead)
#         value, actions = maximize(next_board, cur_board, 3 - piecetype, depth - 1, alpha, beta)
#         value += (numofenemydeadpieces * 5)
#         value -= (numofmydeadpieces * (17/2))
#         # value = curr score, min = best score
#
#         # find min cause minimiser
#         if value < min:
#             min = value
#             minaction = [move] + actions
#
#         # prune
#         if min <= alpha:
#             return min, minaction
#
#         if min < beta:
#             alpha = min
#
#     return min, minaction
#
# if os.path.isfile("output.txt"):
#     os.remove("output.txt")
# boardsize, previousb, currentb, maxint = 5, [], [], float('inf')
# f = open('input.txt', 'r')
# lines = f.read().split('\n')
# previousb = [[int(x) for x in line.rstrip('\n')] for line in lines[1:6]]
# currentb = [[int(x) for x in line.rstrip('\n')] for line in lines[6:11]]
# depth, piecetype = 4, int(lines[0])
# score, actions = maximize(currentb, previousb, piecetype, depth, -maxint, maxint)
# if len(actions) > 0:
#     action = actions[0]
# else:
#     action = "PASS"
# f = open("output.txt", "w")
# if action != "PASS":
#     f.write(str(action[0]))
#     f.write(',')
#     f.write(str(action[1]))
# else:
#     f.write("PASS")
# f.close()

#
# from copy import deepcopy
#
# file1 = open('input.txt', 'r')
# L = file1.readlines()
# col = int(L[0][0])
#
# board = [[]]
# k = 0
# for i in L[6:len(L)]:
#     for j in range(0, 5):
#         board[k].append(int(i[j]))
#     k += 1
#     board.append([])
# board.remove([])
#
# Prev = [[]]
# k = 0
# for i in L[1:len(L) - 5]:
#     for j in range(0, 5):
#         Prev[k].append(int(i[j]))
#     k += 1
#     Prev.append([])
# Prev.remove([])
#
#
# class Gogo:
#
#     def __init__(self, n):
#         self.num = n
#         self.maxcount = 0
#         self.mincount = 0
#
#     def open_adj(self, x, y):
#         adj = []
#         if (x - 1 > -1):
#             adj.append((x - 1, y))
#         if (y - 1 > -1):
#             adj.append((x, y - 1))
#         if (x + 1 < 5):
#             adj.append((x + 1, y))
#         if (y + 1 < 5):
#             adj.append((x, y + 1))
#         return adj
#
#     def get_allies(self, x, y, colour, board):
#         s = [(x, y)]
#         visited = []
#         allies = []
#         visited.append((x, y))
#         while s != []:
#             p = s.pop(0)
#             allies.append(p)
#
#             for coor in self.open_adj(p[0], p[1]):
#                 if (board[coor[0]][coor[1]] == colour):
#                     if coor not in visited:
#                         visited.append(coor)
#                         s.append(coor)
#
#         return allies
#
#     def dead_peices(self, colour, board):
#         dead = []
#         for i in range(0, 5):
#             for j in range(0, 5):
#                 if (board[i][j] == colour):
#                     breaker = False
#                     for allies in self.get_allies(i, j, colour, board):
#                         for adj in self.open_adj(allies[0], allies[1]):
#                             if board[adj[0]][adj[1]] == 0:
#                                 breaker = True
#                                 break
#
#                     if (breaker == False):
#                         dead.append((i, j))
#
#         return dead
#
#     def ally_liberties(self, x, y, colour, board):
#         lib = set()
#         for ally in self.get_allies(x, y, colour, board):
#             for coor in self.open_adj(ally[0], ally[1]):
#                 if board[coor[0]][coor[1]] == 0:
#                     lib.add(coor)
#         return lib
#
#     def make_a_move(self, x, y, colour, board):
#         temp = deepcopy(board)
#         temp[x][y] = colour
#         opp_count = 0
#         my_count = 0
#         opp_dead = self.dead_peices(3 - colour, temp)
#         for i in opp_dead:
#             opp_count += 1
#             temp[i[0]][i[1]] = 0
#         my_dead = self.dead_peices(colour, temp)
#         for i in my_dead:
#             my_count += 1
#             temp[i[0]][i[1]] = 0
#
#         return temp, my_count, opp_count
#
#     def heur(self, colour, B):
#         board = deepcopy(B)
#         bcount = 0
#         wcount = 6
#         bthreat = 0
#         wthreat = 0
#         for i in range(0, 5):
#             for j in range(0, 5):
#                 if (board[i][j] == 1):
#                     bcount += 1
#                     if (len(self.ally_liberties(i, j, 1, board)) <= 1):
#                         bthreat += 1
#                 elif (board[i][j] == 2):
#                     wcount += 1
#                     if (len(self.ally_liberties(i, j, 2, board)) <= 1):
#                         wthreat += 1
#
#         if (colour == 1):
#             return (10 * bcount - 10 * wcount + 2 * wthreat - 1.5 * bthreat)
#         elif (colour == 2):
#             return (10 * wcount - 10 * bcount + 2 * bthreat - 1.5 * wthreat)
#
#     def moveset(self, colour, prev, board):
#         valid = []
#         lib = set()
#         for i in range(0, 5):
#             for j in range(0, 5):
#                 if (board[i][j] != 0):
#                     k = self.ally_liberties(i, j, board[i][j], board)
#                     lib = lib.union((k))
#         #                     print(k)
#         #                     type(k)
#         #                     input()
#
#         # print(lib)
#         # input()
#
#         for i in lib:
#             updated, my_count, opp_count = self.make_a_move(i[0], i[1], colour, board)
#             pu = opp_count - my_count
#             if updated != board and updated != prev:
#                 valid.append((i, pu))
#
#         valid = sorted(valid, key=lambda x: -x[1])
#
#         valid_moves = []
#         for i in valid:
#             valid_moves.append(i[0])
#
#         return valid_moves
#
#     def count_pieces(self, board):
#         bcount = 0
#         wcount = 0
#         for i in range(0, 5):
#             for j in range(0, 5):
#                 if (board[i][j] == 1):
#                     bcount += 1
#                 elif (board[i][j] == 2):
#                     wcount += 1
#
#         return bcount, wcount
#
#     def maxi(self, board, P, colour, depth, alpha, beta):
#         if (depth == 0):
#             return self.heur(colour, board), []
#         bcount, wcount = self.count_pieces(board)
#         if colour == 1:
#             my_count = bcount
#             opp_count = wcount
#         elif colour == 2:
#             my_count = wcount
#             opp_count = bcount
#
#         if opp_count == 0 and my_count == 0:
#             return 100, [(2, 2)]
#         if opp_count == 1 and my_count == 0:
#             if board[2][2] == 3 - colour:
#                 return 100, [(2, 1)]
#             else:
#                 return 100, [(2, 2)]
#
#         maxx = float("-inf")
#         move = []
#         M = self.moveset(colour, P, board)
#         #print(M)
#         for m in M:
#             B = deepcopy(board)
#             new, my_dead, opp_dead = self.make_a_move(m[0], m[1], colour, B)
#             heur, getm = self.mini(new, board, 3 - colour, depth - 1, alpha, beta)
#             heur += opp_dead * 5 - my_dead * 8.5
#             if (heur > maxx):
#                 maxx = heur
#                 move = [m] + getm
#
#             if (maxx >= beta):
#                 return maxx, move
#             if (maxx > alpha):
#                 alpha = maxx
#         return maxx, move
#
#     def mini(self, board, P, colour, depth, alpha, beta):
#         if (depth == 0):
#             return self.heur(colour, board), []
#         bcount, wcount = self.count_pieces(board)
#         if colour == 1:
#             my_count = bcount
#             opp_count = wcount
#         elif colour == 2:
#             my_count = wcount
#             opp_count = bcount
#         if opp_count == 0 and my_count == 0:
#             return 100, [(2, 2)]
#         if opp_count == 1 and my_count == 0:
#             if board[2][2] == 3 - colour:
#                 return 100, [(2, 1)]
#             else:
#                 return 100, [(2, 2)]
#         minn = float("inf")
#         move = []
#         M = self.moveset(colour, P, board)
#         for m in M:
#             B = deepcopy(board)
#             new, my_dead, opp_dead = self.make_a_move(m[0], m[1], colour, B)
#             heur, getm = self.maxi(new, board, 3 - colour, depth - 1, alpha, beta)
#             heur += opp_dead * 5 - my_dead * 8.5
#             if (heur < minn):
#                 minn = heur
#                 move = [m] + getm
#             if (minn <= alpha):
#                 return minn, move
#             if (minn < beta):
#                 alpha = heur
#         return minn, move
#
#
# Work = deepcopy(board)
# moves = Gogo(2)
# meh, move = moves.maxi(Work, Prev, col, 2, float("-inf"), float("inf"))
#
# with open("output.txt", 'w') as fout:
#     if (move == [()] or move == ()):
#         fout.write("PASS")
#     else:
#         fout.write(str(move[0][0]) + ',' + str(move[0][1]))

