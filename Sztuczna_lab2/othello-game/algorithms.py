def min_max(board, player, depth, heuristic):
    if depth == 0:
        return None, heuristic(board, player)

    moves = board.get_legal_moves()
    if len(moves) == 0:
        return None, heuristic(board, player)

    if board.current_player == player:
        best_move = None
        best_score = float('-inf')
        for move in moves:
            board.move = move
            board.make_move_without_drawing()
            a = min_max(board, player, depth - 1, heuristic)
            some_move, score = a
            if score > best_score:
                best_move = move
                best_score = score
        return best_move, best_score
    else:
        best_move = None
        best_score = float('inf')
        for move in moves:
            board.move = move
            board.make_move_without_drawing()
            some_move, score = min_max(board, player, depth - 1, heuristic)
            if score < best_score:
                best_move = move
                best_score = score
        return best_move, best_score
