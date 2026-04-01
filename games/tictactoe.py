import pygame
import numpy as np
from game import Game

CELL_SIZE = 60
GRID_SIZE = 10
WINDOW_SIZE = CELL_SIZE * GRID_SIZE

class TicTacToe(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.current_player = 1  # 1 = X, 2 = O
        self.winner = None

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Tic Tac Toe 10x10 (5 in a row)")
        self.font = pygame.font.SysFont(None, 40)

    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        for i in range(GRID_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, i * CELL_SIZE),
                             (WINDOW_SIZE, i * CELL_SIZE))
            pygame.draw.line(self.screen, (0, 0, 0),
                             (i * CELL_SIZE, 0),
                             (i * CELL_SIZE, WINDOW_SIZE))

    def draw_marks(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == 1:
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (c * CELL_SIZE + 10, r * CELL_SIZE + 10),
                                     (c * CELL_SIZE + CELL_SIZE - 10, r * CELL_SIZE + CELL_SIZE - 10), 3)
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (c * CELL_SIZE + CELL_SIZE - 10, r * CELL_SIZE + 10),
                                     (c * CELL_SIZE + 10, r * CELL_SIZE + CELL_SIZE - 10), 3)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, (0, 0, 255),
                                       (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 10, 3)

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def handle_click(self, pos):
        x, y = pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE

        if self.board[row][col] == 0 and self.winner is None:
            self.board[row][col] = self.current_player

            if self.check_win(row, col):
                self.winner = self.current_player
                print(f"Player {self.current_player} wins!")

            self.switch_turn()

    def check_direction(self, row, col, dr, dc):
        count = 1
        player = self.board[row][col]

        # forward
        r, c = row + dr, col + dc
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc

        # backward
        r, c = row - dr, col - dc
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        return count >= 5

    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        return any(self.check_direction(row, col, dr, dc) for dr, dc in directions)

    def run(self):
        running = True

        while running:
            self.draw_grid()
            self.draw_marks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            pygame.display.flip()

        pygame.quit()