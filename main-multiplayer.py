import socket
import pickle

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
    def __init__(self):
        self.player1 = 1
        self.player2 = 2
        self.current_player = 1
        self.who_am_i = 0
        self.replay = True
        while self.replay:
            host_choice = input("Do you want to host a game? (y/n): ").upper()
            if host_choice == 'Y':
                # Host a game
                host_ip = socket.gethostbyname(socket.gethostname())
                print("Your IP address is:", host_ip)
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind((host_ip, 12345))
                server_socket.listen(1)
                print("Waiting for a player to join...")
                client_socket, address = server_socket.accept()
                print(f"{self.player2} has joined the game.")
                self.who_am_i = 1

            else:
                # Join a game
                host_ip = input("Enter the IP address of the host: ")
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host_ip, 12345))
                print("Connected to the host.")
                self.who_am_i = 2

            board = [[str(i*SIZE+j+1) for j in range(SIZE)] for i in range(SIZE)]
            print("\033[H\033[J", end="")
            printBoard(board)

            while True:
                if self.current_player == 1:
                    if self.who_am_i == 1:
                        choice = getMove(board, self.current_player)

                        # Update the board with the player's move
                        row = (choice - 1) // SIZE
                        col = (choice - 1) % SIZE
                        board[row][col] = 'X'

                        # Check if the current player has won or draw
                        if checkWin(board, 'X'):
                            print(f"Congratulations! Player {self.current_player} has won.")
                            client_socket.send('GAME_OVER'.encode())
                            break
                        elif checkDraw(board):
                            print("The game is a draw")
                            client_socket.send('GAME_OVER'.encode())
                            break

                        print("\033[H\033[J", end="")
                        printBoard(board)

                        # Switch to next player
                        self.current_player = 2 if self.current_player == 1 else 1
                        encoded_board = pickle.dumps(board)
                        client_socket.send(encoded_board)
                    else:
                        print(f"Waiting for Player {self.player1}")
                        data = client_socket.recv(1024)
                        encoded_board = data
                        board = pickle.loads(encoded_board)
                        print("\033[H\033[J", end="")
                        printBoard(board)
                        if checkWin(board, 'O'):
                            print(f"{self.player2} has won.")
                            client_socket.send('GAME_OVER'.encode())
                            break
                        elif checkDraw(board):
                            print("The game is a draw")
                            client_socket.send('GAME_OVER'.encode())
                            break
                        self.current_player = 2 if self.current_player == 1 else 1
                else:
                    if self.who_am_i == 2:
                        choice = getMove(board, self.current_player)

                        # Update the board with the player's move
                        row = (choice - 1) // SIZE
                        col = (choice - 1) % SIZE
                        board[row][col] = 'O'

                        # Check if the current player has won or draw
                        if checkWin(board, 'O'):
                            print(f"Congratulations! Player {self.current_player} has won.")
                            client_socket.send('GAME_OVER'.encode())
                            break
                        elif checkDraw(board):
                            print("The game is a draw")
                            client_socket.send('GAME_OVER'.encode())
                            break

                        print("\033[H\033[J", end="")
                        printBoard(board)

                        # Switch to next player
                        self.current_player = 2 if self.current_player == 1 else 1
                        encoded_board = pickle.dumps(board)
                        client_socket.send(encoded_board)
                    else:
                        print(f"Waiting for Player {self.player1}")
                        data = client_socket.recv(1024)
                        encoded_board = data
                        board = pickle.loads(encoded_board)
                        print("\033[H\033[J", end="")
                        printBoard(board)
                        if checkWin(board, 'O'):
                            print(f"{self.player2} has won.")
                            client_socket.send('GAME_OVER'.encode())
                            break
                        elif checkDraw(board):
                            print("The game is a draw")
                            client_socket.send('GAME_OVER'.encode())
                            break
                        self.current_player = 2 if self.current_player == 1 else 1

            replay_choice = input("Do you want to play again? (y/n): ").upper()
            if replay_choice == 'Y':
                self.replay = True
            else:
                self.replay = False

        # Close the sockets
        client_socket.close()
        if host_choice == 'Y':
            server_socket.close()

if __name__ == "__main__":
    game()
