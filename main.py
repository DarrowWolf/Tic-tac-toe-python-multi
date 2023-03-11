import socket


SIZE = 3

board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

def printBoard(board):
    print("\n\n")
    print("\t\t\t {} | {} | {} \n".format(board[0][0], board[0][1], board[0][2]))
    print("\t\t\t-----------\n")
    print("\t\t\t {} | {} | {} \n".format(board[1][0], board[1][1], board[1][2]))
    print("\t\t\t-----------\n")
    print("\t\t\t {} | {} | {} \n\n".format(board[2][0], board[2][1], board[2][2]))


def getMove(board, player):
    choice = input("Player {}, enter the number of the cell where you want to place your symbol: ".format(player))

    while not choice.isdigit():
        print("Choose a valid value")
        choice = input("Enter your choice: ")

    choice = int(choice)
        
    row = (choice - 1) // SIZE
    col = (choice - 1) % SIZE

    # Check if the chosen position is valid and available
    if choice >= 1 and choice <= 9 and board[row][col] != 'X' and board[row][col] != 'O':
        return choice
    else:
        print("Invalid move. Please try again.\n")
        return getMove(board, player) # Recursively call this function until a valid move is entered

def checkWin(board, symbol):
    # Check rows
    for i in range(SIZE):
        if board[i][0] == symbol and board[i][1] == symbol and board[i][2] == symbol:
            return True # Player has won by completing a row

    # Check columns
    for j in range(SIZE):
        if board[0][j] == symbol and board[1][j] == symbol and board[2][j] == symbol:
            return True # Player has won by completing a column

    # Check diagonal
    if board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol:
        return True # Diagonal check from top-left to bottom-right

    if board[0][2] == symbol and board[1][1] == symbol and board[2][0] == symbol:
        return True # Diagonal check from top-right to bottom-left

    return False # Game is not over yet

def checkDraw(board):
    # Check for a draw
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] != 'X' and board[i][j] != 'O':
                return False # Game is not over yet

    # No more moves left, so the game is a draw
    return True

class game():
    replay = True
    while replay:
        board = [[str(i*SIZE+j+1) for j in range(SIZE)] for i in range(SIZE)]
        player = 1
        printBoard(board)
        while True:
            choice = getMove(board, player)

            # Update the board with the player's move
            row = (choice - 1) // SIZE
            col = (choice - 1) % SIZE
            board[row][col] = 'X' if player == 1 else 'O'

            # Print the updated board and remove previous board so it won't clog up the console
            print("\033[H\033[J", end="")
            printBoard(board)

            # Check if the current player has won or draw
            if checkWin(board, 'X' if player == 1 else 'O'):
                print("Congratulations! Player {} has won.".format(player))
                break
            elif checkDraw(board):
                print("The game is a draw")
                break 

            # Switch to the other player
            player = 2 if player == 1 else 1

        # Ask if the player wants to play again
        replayChoice = input("Do you want to play again? (y/n): ").upper()
        if replayChoice != 'Y':
            replay = False

if __name__ == "__main__":
    ()
