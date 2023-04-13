def more_tiles(board, player):
    score = 0
    for row in range(board.n):
        for col in range(board.n):
            if board.board[row][col] == player + 1:
                score += 1
            elif board.board[row][col] == (player + 2) % 2:
                score -= 1
    return score
