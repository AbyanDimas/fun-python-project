import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] 
== player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] 
== player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]


def minimax(board, depth, is_maximizing, ai_player, human_player):
    if check_winner(board, ai_player):
        return 10 - depth
    if check_winner(board, human_player):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        max_eval = float("-inf")
        for i, j in get_empty_cells(board):
            board[i][j] = ai_player
            score = minimax(board, depth + 1, False, ai_player, 
human_player)
            board[i][j] = " "
            max_eval = max(max_eval, score)
        return max_eval
    else:
        min_eval = float("inf")
        for i, j in get_empty_cells(board):
            board[i][j] = human_player
            score = minimax(board, depth + 1, True, ai_player, 
human_player)
            board[i][j] = " "
            min_eval = min(min_eval, score)
        return min_eval

def get_best_move(board, ai_player, human_player):
    best_score = float("-inf")
    best_move = None
    for i, j in get_empty_cells(board):
        board[i][j] = ai_player
        score = minimax(board, 0, False, ai_player, human_player)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print("Choose game mode:")
    print("1. Play against AI")
    print("2. Play with a friend")

    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice in [1, 2]:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if choice == 1:
        human_player = input("Choose your symbol (X or O): ").upper()
        ai_player = "O" if human_player == "X" else "X"
        print(f"You are {human_player}. AI is {ai_player}.")
        turn = 0  # 0 for human, 1 for AI

        while True:
            print_board(board)
            if check_winner(board, ai_player):
                print("AI wins!")
                break
            if check_winner(board, human_player):
                print("You win!")
                break
            if is_draw(board):
                print("It's a draw!")
                break

            if turn % 2 == 0:
                print("Your turn. Enter row and column (0-2):")
                while True:
                    try:
                        row, col = map(int, input().split())
                        if board[row][col] == " ":
                            board[row][col] = human_player
                            break
                        else:
                            print("Cell already occupied!")
                    except (ValueError, IndexError):
                        print("Invalid input. Try again.")
            else:
                print("AI's turn...")
                row, col = get_best_move(board, ai_player, human_player)
                board[row][col] = ai_player

            turn += 1
    else:
        players = ["X", "O"]
        turn = 0

        while True:
            print_board(board)
            player = players[turn % 2]
            print(f"{player}'s Turn. Enter row and column (0-2): ")

            try:
                row, col = map(int, input().split())
                if board[row][col] == " ":
                    board[row][col] = player
                    if check_winner(board, player):
                        print_board(board)
                        print(f"Player {player} wins!")
                        return
                    if is_draw(board):
                        print_board(board)
                        print("It's a draw!")
                        return
                    turn += 1
                else:
                    print("Cell already occupied!")
            except (ValueError, IndexError):
                print("Invalid input. Try again.")

    print_board(board)

tic_tac_toe()

