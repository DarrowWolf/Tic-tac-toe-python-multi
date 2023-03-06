import numpy as np



board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

def print_board(board):
    print("\n\n")
    print("\t\t\t {} | {} | {} \n".format(board[0][0], board[0][1], board[0][2]))
    print("\t\t\t-----------\n")
    print("\t\t\t {} | {} | {} \n".format(board[1][0], board[1][1], board[1][2]))
    print("\t\t\t-----------\n")
    print("\t\t\t {} | {} | {} \n\n".format(board[2][0], board[2][1], board[2][2]))
    return


print(print_board(board)) #test print for the board

#Players = [("Player 1"), ("Player 2")]

class gamePlay:
    def get_move(board):
        