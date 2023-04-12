# Applies a move to the board and returns the new board.
import copy


# Initialize the Othello board
def initialize_board():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3], board[4][4] = 1, 1
    board[3][4], board[4][3] = -1, -1
    return board


# Print the Othello board
def print_board(board):
    print("   ", end="")
    for i in range(8):
        print(i, end=" ")
    print()
    print("  +-----------------+")
    for i in range(8):
        print(i, "|", end=" ")
        for j in range(8):
            if board[i][j] == 1:
                print("●", end=" ")
            elif board[i][j] == -1:
                print("○", end=" ")
            else:
                print(" ", end=" ")
        print("|")
    print("  +-----------------+")


# Get the list of valid moves for a player
def get_valid_moves(board, player):
    valid_moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                for xdir, ydir in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    x, y = i + xdir, j + ydir
                    flips = []
                    while 0 <= x < 8 and 0 <= y < 8 and board[x][y] == -player:
                        flips.append((x, y))
                        x += xdir
                        y += ydir
                    if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == player and flips:
                        valid_moves.append((i, j))
                        break
    return valid_moves


# Apply a move on the board and flip the opponent's pieces
def apply_move(board, move, player):
    x, y = move
    new_board = copy.deepcopy(board)
    new_board[x][y] = player
    for xdir, ydir in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        i, j = x + xdir, y + ydir
        flips = []
        if player is None:
            new_board[i][j] = " "
            return new_board
        while 0 <= i < 8 and 0 <= j < 8 and new_board[i][j] == -player:
            flips.append((i, j))
            i += xdir
            j += ydir
        if 0 <= i < 8 and 0 <= j < 8 and new_board[i][j] == player:
            for (x, y) in flips:
                new_board[x][y] = player
    return new_board


# Evaluate the score of the current board for a player
def evaluate_board(board, player):
    score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                score += 1
            elif board[i][j] == -player:
                score -= 1
    return score


def play_othello():
    board = initialize_board()
    print_board(board)

    while not game_over(board):
        if len(get_valid_moves(board, 1)) > 0:
            human_move = input("Enter your move (x,y): ")
            x, y = map(int, human_move.split(','))
            if (x, y) in get_valid_moves(board, 1):
                board = apply_move(board, (x, y), 1)
            else:
                print("Invalid move, try again.")
                continue
        else:
            print("You have no valid moves. Computer's turn.")

        computer_move, _ = minimax(board, 3, True)
        board = apply_move(board, computer_move, -1)
        print(f"Computer played ({computer_move[0]},{computer_move[1]})")
        print_board(board)

    score = get_score(board)
    if score > 0:
        print("You won!")
    elif score < 0:
        print("Computer won!")
    else:
        print("It's a tie!")


def minimax(board, depth, maximizing_player):
    if depth == 0 or game_over(board):
        return None, evaluate_board(board, maximizing_player)
    if maximizing_player:
        best_value = float('-inf')
        best_move = None
        for move in get_valid_moves(board, 1):
            new_board = apply_move(board, move, 1)
            _, value = minimax(new_board, depth - 1, False)
            if value > best_value:
                best_value = value
                best_move = move
            board = apply_move(board, move, None)
        return best_move, best_value
    else:
        best_value = float('inf')
        best_move = None
        for move in get_valid_moves(board, -1):
            new_board = apply_move(board, move, -1)
            _, value = minimax(new_board, depth - 1, True)
            if value < best_value:
                best_value = value
                best_move = move
            board = apply_move(board, move, None)
        return best_move, best_value


def game_over(board):
    return len(get_valid_moves(board, 1)) == 0 and len(get_valid_moves(board, -1)) == 0 or is_board_full(board)


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True


def get_score(board):
    player1_score = 0
    player2_score = 0
    for row in board:
        for cell in row:
            if cell == 1:
                player1_score += 1
            elif cell == -1:
                player2_score += 1
    return player1_score, player2_score

def get_best_move(board, player):
    valid_moves = get_valid_moves(board, player)
    if not valid_moves:
        return None, evaluate_board(board, player)
    best_move = valid_moves[0]
    best_score = float('-inf')
    for move in valid_moves:
        new_board = apply_move(board, move, player)
        _, score = minimax(new_board, 3, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move, best_score



if __name__ == '__main__':
    board = initialize_board()
    print_board(board)

    player = 1
    computer = -1

    while not game_over(board):
        if player == 1:
            valid_moves = get_valid_moves(board, player)
            if valid_moves:
                print(f"Valid moves: {valid_moves}")
                move = input("Enter your move (x,y): ")
                x, y = map(int, move.split(","))
                if (x, y) in valid_moves:
                    board = apply_move(board, (x, y), player)
                    print_board(board)
                    player, computer = computer, player
                else:
                    print("Invalid move. Try again.")
            else:
                print("No valid moves. Turn skipped.")
                player, computer = computer, player
        else:
            print("Computer thinking...")
            move = get_best_move(board, computer)
            print(f"Computer moves: {move}")
            board = apply_move(board, move[0], computer)
            print_board(board)
            player, computer = computer, player

    score = get_score(board)[0]
    if score > 0:
        print("You win!")
    elif score < 0:
        print("Computer wins!")
    else:
        print("It's a tie!")
