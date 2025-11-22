def print_board(board):
    print("---------")
    for i in range(3):
        print("|", board[i][0], "|", board[i][1], "|", board[i][2], "|")
    print("---------")

def check_win(board, player):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def check_tie(board):
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True

def play_game():
    board = [["" for _ in range(3)] for _ in range(3)]
    player = "X"

    while True:
        print_board(board)
        print(f"Player {player}, it's your turn.")

        while True:
            try:
                row = int(input("Enter row (0–2): "))
                col = int(input("Enter column (0–2): "))
                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == "":
                    break
                else:
                    print("Invalid move. Try again.")    
            except ValueError:
                print("Invalid input. Please enter a number.")


        board[row][col] = player
        if check_win(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break
        if check_tie(board):
            print_board(board)
            print("It's a tie!")
            break

        player = "O" if player == "X" else "X"
if __name__ == "__main__":
    play_game()
# tic-tac-toe.py end
