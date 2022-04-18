import os


def neighbor(i, j):  # done
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


def copy(board):  # done
    new_board = []
    for i in range(boardsize):
        new_board.append([])
    for i in range(boardsize):
        for j in range(boardsize):
            new_board[i].append(board[i][j])
    return new_board


def chains(i, j, board, piecetype):
    vis, stack, chain = {}, [(i, j)], []
    vis[(i, j)] = True
    while stack:
        cur = stack.pop()
        chain.append(cur)
        for n in neighbor(cur[0], cur[1]):
            if board[n[0]][n[1]] == piecetype and n not in vis:
                stack.append(n)
                vis[n] = True
    return chain


def dead_pieces(piecetype, board):  # done
    dead, lib = [], False
    for a in range(0, boardsize):
        for b in range(0, boardsize):
            if piecetype == board[a][b]:
                c = chains(a, b, board, piecetype)
                for piece in c:
                    n = neighbor(piece[0], piece[1])
                    for nei in n:
                        b = board[nei[0]][nei[1]]
                        if b == 0:
                            lib = True
                if not lib:
                    dead.append((a, b))
    return dead


def positionofliberty(i, j, board, piecetype):  # done
    c, liberties = chains(i, j, board, piecetype), set()
    for piece in c:
        nei = neighbor(piece[0], piece[1])
        for n in nei:
            b = board[n[0]][n[1]]
            if b == 0:
                liberties.add(n)
    return liberties


def evaluation(board, piecetype):  # done
    whitepieces, whitedanger, blackpieces, blackdanger = 3, 0, -3, 0
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if board[i][j] == 2:
                lib_count = len(positionofliberty(i, j, board, 2))
                if lib_count <= 1:
                    whitedanger += 1
                whitepieces += 1
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if board[i][j] == 1:
                lib_count = len(positionofliberty(i, j, board, 1))
                if lib_count <= 1:
                    blackdanger += 1
                blackpieces += 1
    # white
    if piecetype == 1:
        p1 = (10 * blackpieces) - (10 * whitepieces)
        p2 = (2 * whitedanger) - ((3 / 2) * blackdanger)
        eval = p1 + p2
        # p1 = blackpieces - whitepieces
        # p2 = whitedanger - 2*blackdanger
        # eval = p1 + p2
    elif piecetype == 2:
        p1 = (10 * whitepieces) - (10 * blackpieces)
        p2 = (2 * blackdanger) - ((3 / 2) * whitedanger)
        eval = p1 + p2
        # p1 = whitepieces - blackpieces
        # p2 = blackdanger - 2*whitedanger
        # eval = p1 + p2
    return eval


def bestmoves(piecetype, prev_board, cur_board):
    best, all_moves = [], set()
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if not (cur_board[i][j] == 0):
                all_moves |= positionofliberty(i, j, cur_board, cur_board[i][j])
    for pos in all_moves:
        cp = copy(cur_board)
        cp[pos[0]][pos[1]] = piecetype
        enemydead, mydead = dead_pieces(3 - piecetype, cp), dead_pieces(piecetype, cp)
        for piece in enemydead:
            cp[piece[0]][piece[1]] = 0
        for piece in mydead:
            cp[piece[0]][piece[1]] = 0
        board_after_move, numofmydeadpieces, numofenemydeadpieces = cp, len(mydead), len(enemydead)
        if not (board_after_move == cur_board):
            if not (board_after_move == prev_board):
                diff = numofenemydeadpieces - numofmydeadpieces
                best.append((pos[0], pos[1], diff))
    l = len(best)
    if not (l == 0):
        return sorted(best, key=lambda x: -x[2])
    return None


# def minimax(currentb, previousb, piecetype, depth, alpha, beta):
#     enemypieces = mypieces = 0
#     max, min = -maxint, maxint
#     if depth == 0:
#         return evaluation(currentb, piecetype), []
#     for i in range(boardsize):
#         for j in range(boardsize):
#             if currentb[i][j] == 3 - piecetype:
#                 enemypieces = enemypieces + 1
#             if currentb[i][j] == piecetype:
#                 mypieces = mypieces + 1
#     if enemypieces == mypieces == 0:
#         return 100, [(2, 2)]
#     if mypieces == 0:
#         if enemypieces == 1:
#             if currentb[2][2] == 3 - piecetype:
#                 return 100, [(2, 1)]
#             else:
#                 return 100, [(2, 2)]
#     mymoves = bestmoves(piecetype, previousb, currentb)
#     maxaction, minaction = [], []
#     for move in mymoves:
#         cp = copy(currentb)
#         cp[move[0]][move[1]] = piecetype
#         enemydead, mydead = dead_pieces(3 - piecetype, cp), dead_pieces(piecetype, cp)
#         for piece in enemydead:
#             cp[piece[0]][piece[1]] = 0
#         for piece in mydead:
#             cp[piece[0]][piece[1]] = 0
#         next_board, numofmydeadpieces, numofenemydeadpieces = cp, len(mydead), len(enemydead)
#         value, actions = minimax(next_board, currentb, 3 - piecetype, depth - 1, alpha, beta)
#         value += (numofenemydeadpieces * 5)
#         value -= (numofmydeadpieces * (17 / 2))
#         if max >= beta:
#             return max, maxaction
#         if min <= alpha:
#             return min, minaction
#         if value > max:
#             max, maxaction = value, [move] + actions
#         if max > alpha:
#             alpha = max
#         if value < min:
#             min = value
#             minaction = [move] + actions
#         if min < beta:
#             alpha = min
#     return max, maxaction


def maximize(currentb, previousb, piecetype, depth, alpha, beta):
    enemypieces = mypieces = 0
    if depth == 0:
        return evaluation(currentb, piecetype), []
    # Counting player and opponent pieces
    for i in range(boardsize):
        for j in range(boardsize):
            if currentb[i][j] == 3 - piecetype:
                enemypieces = enemypieces + 1
            if currentb[i][j] == piecetype:
                mypieces = mypieces + 1

    if enemypieces == mypieces == 0:
        return 100, [(2, 2)]

    if mypieces == 0:
        if enemypieces == 1:
            if currentb[2][2] == 3 - piecetype:
                return 100, [(2, 1)]
            else:
                return 100, [(2, 2)]
    mymoves = bestmoves(piecetype, previousb, currentb)
    # shuffle(mymoves)

    max = -maxint
    maxaction = []
    for move in mymoves:
        '''
        1. score for each move
        2. getting the min of all scores
        3. prune
        '''
        cp = copy(currentb) # copy board
        cp[move[0]][move[1]] = piecetype # place  move
        enemydead, mydead = dead_pieces(3 - piecetype, cp), dead_pieces(piecetype, cp) # dead pieces

        for piece in enemydead:
            cp[piece[0]][piece[1]] = 0
        for piece in mydead:
            cp[piece[0]][piece[1]] = 0
        next_board, numofmydeadpieces, numofenemydeadpieces = cp, len(mydead), len(enemydead)


        value, actions = minimize(next_board, currentb, 3 - piecetype, depth - 1, alpha, beta)
        # value += (numofenemydeadpieces * 5)
        # value -= (numofmydeadpieces * (17/2))

        #  finding max score cause maximiser
        if value > max:
            max, maxaction = value, [move] + actions

        # prune
        if max >= beta:
            return max, maxaction

        if max > alpha:
            alpha = max

    return max, maxaction


def minimize(cur_board, prev_board, piecetype, depth, alpha, beta):
    enemypieces = mypieces = 0
    min = maxint

    if depth == 0:
        return evaluation(cur_board, piecetype), []

    for i in range(boardsize):
        for j in range(boardsize):
            if cur_board[i][j] == 3 - piecetype:
                enemypieces += 1
            if cur_board[i][j] == piecetype:
                mypieces += 1
    if enemypieces == mypieces == 0:
        return 100, [(2, 2)]
    if mypieces == 0:
        if enemypieces == 1:
            if cur_board[2][2] == 3 - piecetype:
                return 100, [(2, 1)]
            else:
                return 100, [(2, 2)]

    my_moves = bestmoves(piecetype, prev_board, cur_board)

    print(my_moves)

    minaction = []
    for move in my_moves:
        cp = copy(cur_board)
        cp[move[0]][move[1]] = piecetype
        enemydead, mydead = dead_pieces(3 - piecetype, cp), dead_pieces(piecetype, cp)
        for piece in enemydead:
            cp[piece[0]][piece[1]] = 0
        for piece in mydead:
            cp[piece[0]][piece[1]] = 0


        next_board, numofmydeadpieces, numofenemydeadpieces = cp, len(mydead), len(enemydead)
        value, actions = maximize(next_board, cur_board, 3 - piecetype, depth - 1, alpha, beta)
        # value += (numofenemydeadpieces * 5)
        # value -= (numofmydeadpieces * (17/2))
        # value = curr score, min = best score

        # find min cause minimiser
        if value < min:
            min = value
            minaction = [move] + actions

        # prune
        if min <= alpha:
            return min, minaction

        if min < beta:
            beta = min

    return min, minaction

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
score, actions = maximize(currentb, previousb, piecetype, depth, -maxint, maxint)
if len(actions) > 0:
    action = actions[0]
else:
    action = "PASS"
f = open("output.txt", "w")
if action != "PASS":
    f.write(str(action[0]))
    f.write(',')
    f.write(str(action[1]))
else:
    f.write("PASS")
f.close()


