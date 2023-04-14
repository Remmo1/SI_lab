def min_max(board, player, depth, heuristic, nodes_visited=0):
    nodes_visited += 1

    if depth == 0:
        return None, heuristic(board, player), nodes_visited

    moves = board.get_legal_moves()
    if len(moves) == 0:
        return None, heuristic(board, player), nodes_visited

    if board.current_player == player:
        best_move = None
        best_score = float('-inf')
        for move in moves:
            board.move = move
            board.make_move_without_drawing()
            # board.current_player = change_player(player)
            some_move, score, nodes = min_max(board, change_player(player), depth - 1, heuristic, nodes_visited)
            if score > best_score:
                best_move = move
                best_score = score
            nodes_visited += nodes
        return best_move, best_score, nodes_visited
    else:
        best_move = None
        best_score = float('inf')
        for move in moves:
            board.move = move
            board.make_move_without_drawing()
            # board.current_player = change_player(player)
            some_move, score, nodes = min_max(board, change_player(player), depth - 1, heuristic, nodes_visited)
            if score < best_score:
                best_move = move
                best_score = score
            nodes_visited += nodes
        return best_move, best_score, nodes_visited


def alfa_beta(board, player, depth, heuristic, alpha=float('-inf'), beta=float('inf'), nodes_visited=0):
    nodes_visited += 1

    if depth == 0:
        return None, heuristic(board, player), nodes_visited

    moves = board.get_legal_moves()
    if len(moves) == 0:
        return None, heuristic(board, player), nodes_visited

    if board.current_player == player:
        best_move = None
        best_score = float('-inf')
        for move in moves:
            board.move = move
            board.make_move_without_drawing()
            some_move, score, nodes = alfa_beta(
                board, change_player(player), depth - 1, heuristic, alpha, beta, nodes_visited
            )
            if score > best_score:
                best_move = move
                best_score = score
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

            nodes_visited += nodes

        return best_move, best_score, nodes_visited
    else:
        best_move = None
        best_score = float('inf')
        for move in moves:
            board.move = move
            board.make_move_without_drawing()
            some_move, score, nodes = alfa_beta(
                board, change_player(player), depth - 1, heuristic, alpha, beta, nodes_visited
            )
            if score < best_score:
                best_move = move
                best_score = score
            beta = min(beta, best_score)

            if beta <= alpha:
                break

            nodes_visited += nodes
        return best_move, best_score, nodes_visited


def change_player(player):
    if player == 0:
        return 1
    else:
        return 0
