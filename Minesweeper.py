from Constants import *
from random import randint

def create_board():
    board = [[UNDISCOVERED for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]
    generate_bombs(board)
    return board

def generate_bombs(board):
    remaining = int(BOARD_ROWS * BOARD_COLUMNS * BOARD_BOMB_PERCENTAGE) 

    while remaining:
        row = randint(0, BOARD_ROWS - 1)
        column = randint(0, BOARD_COLUMNS - 1)

        if board[row][column] == UNDISCOVERED:
            board[row][column] = BOMB
            remaining -= 1

def is_bomb(board, row, column):
    if row < 0 or column < 0 or row >= BOARD_ROWS or column >= BOARD_COLUMNS:
        return 0
    return board[row][column] == BOMB

def reveal(board, row, column):
    if row < 0 or column < 0 or row >= BOARD_ROWS or column >= BOARD_COLUMNS:
        return False
    if (board[row][column] == EMPTY):
        return False
    if (board[row][column] == BOMB):
        return True

    count = 0
    for row_offset in range(-1, 2):
        for column_offset in range(-1, 2):
            if row_offset != 0 or column_offset != 0:
                count += is_bomb(board, row + row_offset, column + column_offset)
    
    if count > 0:
        board[row][column] = count
    else:
        board[row][column] = EMPTY
        if (reveal(board, row - 1, column) 
            or reveal(board, row + 1, column)
            or reveal(board, row, column - 1)
            or reveal(board, row, column + 1)):
            return True
    
    return False
