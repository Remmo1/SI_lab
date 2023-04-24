def more_tiles(board, player):
    """
        Heuristic function that returns a score for actual player's situation.
        It counts tiles.

        Parameters:
        - board (Board)     : the current board
        - player (number)   : player for who tiles are counted

        Returns:
        - score (int)       : the score for the move
    """
    score = 0
    for row in range(board.n):
        for col in range(board.n):
            if board.board[row][col] == player + 1:
                score += 1
            elif board.board[row][col] == (player + 2) % 2:
                score -= 1
    return score


def reach_corner(board, player):
    """
    Heuristic function that returns a score for a move based on how close it is
    to a corner. A move that is closer to a corner gets a higher score.

    Parameters:
    - board (Board)     : the current board
    - player (number)   : player for who tiles are counted

    Returns:
    - score (int)       : the score for the move
    """
    corners = [(0, 0), (0, board.n - 1), (board.n - 1, 0), (board.n - 1, board.n - 1)]
    score = 0
    for corner in corners:
        dist = abs(board.move[0] - corner[0]) + abs(board.move[1] - corner[1])
        score += dist
    return score


def tiles_and_corners(board, player):
    """
        Heuristic function that combines two above.
        It takes them to square and adds them.

        Parameters:
        - board (Board)     : the current board
        - player (number)   : player for who tiles are counted

        Returns:
        - score (int)       : the score for the move
        """
    return more_tiles(board, player) ** 2 + reach_corner(board, player) ** 2
