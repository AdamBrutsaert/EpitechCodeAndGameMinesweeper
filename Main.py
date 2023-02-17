import pygame as pg
from Minesweeper import *

RESOURCES = {}

def load_resources():
    font = pg.font.SysFont("Arial", 16)
    RESOURCES["texts"] = [
        font.render("1", True, TEXT_COLOR),
        font.render("2", True, TEXT_COLOR),
        font.render("3", True, TEXT_COLOR),
        font.render("4", True, TEXT_COLOR),
        font.render("5", True, TEXT_COLOR),
        font.render("6", True, TEXT_COLOR),
        font.render("7", True, TEXT_COLOR),
        font.render("8", True, TEXT_COLOR)
    ]
    RESOURCES["bomb"] = pg.image.load("assets/bomb.png").convert_alpha()

def draw_borders(screen):
    for column in range(BOARD_COLUMNS + 1):
        x = PADDING + column * (CELL_SIZE + CELL_BORDER)
        y = PADDING
        width = CELL_BORDER
        height = SCREEN_HEIGHT - 2 * PADDING

        pg.draw.rect(screen, BORDER_COLOR, (x, y, width, height))

    for row in range(BOARD_ROWS + 1):
        x = PADDING 
        y = PADDING + row * (CELL_SIZE + CELL_BORDER)
        width = SCREEN_WIDTH - 2 * PADDING
        height = CELL_BORDER

        pg.draw.rect(screen, BORDER_COLOR, (x, y, width, height))

def draw_cell(screen, board, row, column):
    if board[row][column] == UNDISCOVERED or board[row][column] == BOMB:
        x = PADDING + column * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
        y = PADDING + row * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
        width = CELL_SIZE
        height = CELL_SIZE

        pg.draw.rect(screen, UNDISCOVERED_COLOR, (x, y, width, height))
    elif board[row][column] > 0:
        x = PADDING + column * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
        y = PADDING + row * (CELL_SIZE + CELL_BORDER) + CELL_BORDER

        screen.blit(RESOURCES["texts"][board[row][column] - 1], (x, y))

    if DEBUG and board[row][column] == BOMB:
        x = PADDING + column * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
        y = PADDING + row * (CELL_SIZE + CELL_BORDER) + CELL_BORDER

        screen.blit(RESOURCES["bomb"], (x, y))

def draw(screen, board):
    screen.fill(BACKGROUND_COLOR)

    draw_borders(screen)

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            draw_cell(screen, board, row, column)

    pg.display.flip()

def on_click(board, pos):
    row = (pos[1] - PADDING) / (CELL_SIZE + CELL_BORDER)
    column = (pos[0] - PADDING) / (CELL_SIZE + CELL_BORDER)

    if row < 0 or column < 0 or row >= BOARD_ROWS or column >= BOARD_COLUMNS:
        return False

    return reveal(board, int(row), int(column))

def main():
    pg.init()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    load_resources()
    board = create_board()
    running = True

    draw(screen, board)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                if on_click(board, event.pos):
                    return
                draw(screen, board)

if __name__ == "__main__":
    main()