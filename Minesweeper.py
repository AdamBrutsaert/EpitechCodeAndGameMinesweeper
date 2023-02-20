import pygame as pg
from Constants import *
from random import randint

class Minesweeper:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.load_resources()

        self.create_grid()
        self.generate_mines()

        self.flags = []
        self.hasLost = False

    def load_resources(self):
        font = pg.font.SysFont("Arial", 16)
        self.texts = [
            font.render("1", True, TEXT_COLOR),
            font.render("2", True, TEXT_COLOR),
            font.render("3", True, TEXT_COLOR),
            font.render("4", True, TEXT_COLOR),
            font.render("5", True, TEXT_COLOR),
            font.render("6", True, TEXT_COLOR),
            font.render("7", True, TEXT_COLOR),
            font.render("8", True, TEXT_COLOR)
        ]
        self.mine = pg.image.load("assets/mine.png").convert_alpha()
        self.flag = pg.image.load("assets/flag.png").convert_alpha()

    def draw_borders(self):
        for column in range(GRID_COLUMNS + 1):
            x = PADDING + column * (CELL_SIZE + CELL_BORDER)
            y = PADDING
            width = CELL_BORDER
            height = SCREEN_HEIGHT - 2 * PADDING

            pg.draw.rect(self.screen, BORDER_COLOR, (x, y, width, height))

        for row in range(GRID_ROWS + 1):
            x = PADDING
            y = PADDING + row * (CELL_SIZE + CELL_BORDER)
            width = SCREEN_WIDTH - 2 * PADDING
            height = CELL_BORDER

            pg.draw.rect(self.screen, BORDER_COLOR, (x, y, width, height))

    def draw_cell(self, row, column):
        if self.grid[row][column] == UNDISCOVERED or self.grid[row][column] == MINE:
            x = PADDING + column * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            y = PADDING + row * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            width = CELL_SIZE
            height = CELL_SIZE
            pg.draw.rect(self.screen, UNDISCOVERED_COLOR, (x, y, width, height))
        elif self.grid[row][column] > 0:
            x = PADDING + column * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            y = PADDING + row * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            self.screen.blit(self.texts[self.grid[row][column] - 1], (x, y))

        if self.hasLost and self.grid[row][column] == MINE:
            x = PADDING + column * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            y = PADDING + row * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            self.screen.blit(self.mine, (x, y))

    def draw_flags(self):
        for flag in self.flags:
            x = PADDING + flag[1] * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            y = PADDING + flag[0] * (CELL_SIZE + CELL_BORDER) + CELL_BORDER
            self.screen.blit(self.flag, (x, y))

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_borders()
        for row in range(GRID_ROWS):
            for column in range(GRID_COLUMNS):
                self.draw_cell(row, column)
        if not self.hasLost:
            self.draw_flags()
        pg.display.flip()

    def on_left_click(self, pos):
        if self.hasLost:
            return

        row = (pos[1] - PADDING) / (CELL_SIZE + CELL_BORDER)
        column = (pos[0] - PADDING) / (CELL_SIZE + CELL_BORDER)

        if row < 0 or column < 0 or row >= GRID_ROWS or column >= GRID_COLUMNS:
            return

        if self.reveal(int(row), int(column)):
            self.hasLost = True

    def on_right_click(self, pos):
        if self.hasLost:
            return

        row = (pos[1] - PADDING) / (CELL_SIZE + CELL_BORDER)
        column = (pos[0] - PADDING) / (CELL_SIZE + CELL_BORDER)

        if row < 0 or column < 0 or row >= GRID_ROWS or column >= GRID_COLUMNS:
            return

        row = int(row)
        column = int(column)

        if (row, column) in self.flags or self.grid[row][column] >= 0:
            return
        self.flags += [(row, column)]

    def run(self):
        running = True
        self.draw()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        self.on_left_click(event.pos)
                        self.draw()
                    if event.button == pg.BUTTON_RIGHT:
                        self.on_right_click(event.pos)
                        self.draw()

    def create_grid(self):
        self.grid = [[UNDISCOVERED for column in range(GRID_COLUMNS)] for row in range(GRID_ROWS)]

    def generate_mines(self):
        remaining = int(GRID_ROWS * GRID_COLUMNS * GRID_MINE_PERCENTAGE)

        while remaining:
            row = randint(0, GRID_ROWS - 1)
            column = randint(0, GRID_COLUMNS - 1)

            if self.grid[row][column] == UNDISCOVERED:
                self.grid[row][column] = MINE
                remaining -= 1

    def is_bomb(self, row, column):
        if row < 0 or column < 0 or row >= GRID_ROWS or column >= GRID_COLUMNS:
            return False
        return self.grid[row][column] == MINE

    def reveal(self, row, column):
        if row < 0 or column < 0 or row >= GRID_ROWS or column >= GRID_COLUMNS:
            return False
        if (self.grid[row][column] == EMPTY):
            return False
        if (self.grid[row][column] == MINE):
            return True

        if (row, column) in self.flags:
            self.flags.remove((row, column))

        count = 0
        for row_offset in range(-1, 2):
            for column_offset in range(-1, 2):
                if row_offset != 0 or column_offset != 0:
                    count += self.is_bomb(row + row_offset, column + column_offset)

        if count > 0:
            self.grid[row][column] = count
        else:
            self.grid[row][column] = EMPTY
            self.reveal(row - 1, column)
            self.reveal(row + 1, column)
            self.reveal(row, column - 1)
            self.reveal(row, column + 1)

        return False

if __name__ == "__main__":
    Minesweeper().run()
