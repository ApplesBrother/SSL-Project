import pygame
import numpy as np
from game import Game

GRID_SIZE = 8
CELL_SIZE = 80
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Directions: 8 possible
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

class Othello(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)

        self.board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

        # Initial setup
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2

        self.current_player = 1
        self.winner = None

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Othello")

        self.font = pygame.font.SysFont(None, 40)

    # ---------------- DRAW ---------------- #

    def draw_board(self):
        self.screen.fill((0, 128, 0))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                pygame.draw.rect(
                    self.screen, (0, 0, 0),
                    (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
                )

                if self.board[r][c] != 0:
                    color = (0, 0, 0) if self.board[r][c] == 1 else (255, 255, 255)
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (c * CELL_SIZE + CELL_SIZE // 2,
                         r * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 2 - 10
                    )

    # ---------------- GAME LOGIC ---------------- #

    def in_bounds(self, r, c):
        return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

    def get_flips(self, r, c, player):
        if self.board[r][c] != 0:
            return []

        opponent = 2 if player == 1 else 1
        flips = []

        for dr, dc in DIRECTIONS:
            path = []
            nr, nc = r + dr, c + dc

            while self.in_bounds(nr, nc) and self.board[nr][nc] == opponent:
                path.append((nr, nc))
                nr += dr
                nc += dc

            if self.in_bounds(nr, nc) and self.board[nr][nc] == player and path:
                flips.extend(path)

        return flips

    def has_valid_move(self, player):
        # no explicit loops over board values, just positions
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.get_flips(r, c, player):
                    return True
        return False

    def make_move(self, r, c):
        flips = self.get_flips(r, c, self.current_player)

        if not flips:
            return False

        self.board[r][c] = self.current_player
        for fr, fc in flips:
            self.board[fr][fc] = self.current_player

        return True

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

        # Skip turn if no valid moves
        if not self.has_valid_move(self.current_player):
            self.current_player = 2 if self.current_player == 1 else 1

            # If BOTH players cannot move → game ends
            if not self.has_valid_move(self.current_player):
                self.end_game()

    def end_game(self):
        # NO manual loops — using numpy
        count1 = np.sum(self.board == 1)
        count2 = np.sum(self.board == 2)

        if count1 > count2:
            self.winner = 1
        elif count2 > count1:
            self.winner = 2
        else:
            self.winner = 0  # draw

    # ---------------- UI ---------------- #

    def draw_winner(self):
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        if self.winner == 0:
            text = "Draw!"
        else:
            name = self.player1 if self.winner == 1 else self.player2
            text = f"{name} wins!"

        render = self.font.render(text, True, (255, 255, 255))
        rect = render.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        self.screen.blit(render, rect)

    # ---------------- MAIN LOOP ---------------- #

    def run(self):
        running = True

        while running:
            self.draw_board()

            if self.winner is not None:
                self.draw_winner()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.winner is None:
                        x, y = pygame.mouse.get_pos()
                        r, c = y // CELL_SIZE, x // CELL_SIZE

                        if self.make_move(r, c):
                            self.switch_turn()
                    else:
                        running = False  # click to exit after game

            pygame.display.flip()

        pygame.quit()