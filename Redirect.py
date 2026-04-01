import pygame
import sys

from tictactoe.py import load_tictactoe
from connect4.py import load_connect4
from othello.py import load_othello

pygame.init()

WDT, HGT = 800, 600
screen = pygame.display.set_mode((WDT, HGT))
pygame.display.set_caption("SSL Arcade")

player1 = sys.argv[1] if len(sys.argv) > 1 else "Player 1"
player2 = sys.argv[2] if len(sys.argv) > 2 else "Player 2"

# Phases
MENU = "menu"
SELECT_PLAY = "play"
SELECT_LEADER = "leader"
LEADERBOARD = "leaderboard"

state = MENU
sel_game = None

# Formatting
title_font = pygame.font.SysFont("arial", 64, bold=True)
font = pygame.font.SysFont("arial", 36)
small_font = pygame.font.SysFont("arial", 24)
BG = (15, 18, 30)
BTN = (40, 90, 160)
HOVER = (70, 140, 255)
ACCENT = (255, 215, 0)   # gold accent
WHITE = (240, 240, 240)
SUBTEXT = (180, 180, 200)

#Button Arrays
button_list1 = {
    "Play": pygame.Rect(300, 220, 200, 60),
    "Leaderboard": pygame.Rect(300, 320, 200, 60),
}

button_list2 = {
    "TicTacToe": pygame.Rect(300, 200, 200, 60),
    "Connect4": pygame.Rect(300, 300, 200, 60),
    "Othello": pygame.Rect(300, 400, 200, 60),
}

back_button = pygame.Rect(20, 20, 100, 40)

# Text Format
def draw_text(text, f, x, y, color=WHITE):
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

# Special Button
def draw_button(rect, text):
    if rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, HOVER, rect, border_radius=12)
    else:
        pygame.draw.rect(screen, BTN, rect, border_radius=12)

    draw_text(text, font, rect.centerx, rect.centery)

#Display Scores
def score_load(game):
    scores = []
    try:
        with open(f"{game}.tsv", "r") as f:
            for line in f:
                name, score = line.strip().split("\t")
                scores.append((name, int(score)))
    except:
        pass

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:10]

# Main Lopp
running = True
while running:
    mouse = pygame.mouse.get_pos()
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # MAIN MENU
            if state == MENU:
                if button_list1["Play"].collidepoint(event.pos):
                    state = SELECT_PLAY

                elif button_list1["Leaderboard"].collidepoint(event.pos):
                    state = SELECT_LEADER

            # SELECT GAME
            elif state in [SELECT_PLAY, SELECT_LEADER]:
                for name, rect in button_list2.items():
                    if rect.collidepoint(event.pos):
                        sel_game = name

                        if state == SELECT_PLAY:
                            if name == "TicTacToe":
                                load_tictactoe(screen, player1, player2)
                            elif name == "Connect4":
                                load_connect4(screen, player1, player2)
                            elif name == "Othello":
                                load_othello(screen, player1, player2)
                        else:
                            state = LEADERBOARD

                if back_button.collidepoint(event.pos):
                    state = MENU

            # LEADERBOARD
            elif state == LEADERBOARD:
                if back_button.collidepoint(event.pos):
                    state = MENU

    # DRAWING

    if state == MENU:
        draw_text("SSL Arcade", title_font, WDT//2, 90, ACCENT)

        # Player names
        draw_text(f"{player1} vs {player2}", small_font, WDT//2, 140, SUBTEXT)

        for text, rect in button_list1.items():
            draw_button(rect, text)

        # CONTACT SECTION 👇
        draw_text("Contact: email2rajit@gmail.com", small_font, WDT//2, 520, SUBTEXT)

    elif state in [SELECT_PLAY, SELECT_LEADER]:
        draw_text("Select Game", title_font, WDT//2, 100, ACCENT)

        for text, rect in button_list2.items():
            draw_button(rect, text)

        draw_button(back_button, "Back")

    elif state == LEADERBOARD:
        draw_text(f"{sel_game} Leaderboard", title_font, WDT//2, 80, ACCENT)

        scores = score_load(sel_game.replace(" ", "").lower())

        y = 150
        for i, (name, score) in enumerate(scores):
            color = ACCENT if i == 0 else WHITE  # highlight top player
            text = f"{i+1}. {name} - {score}"
            draw_text(text, small_font, WDT//2, y, color)
            y += 40

        draw_button(back_button, "Back")

    pygame.display.flip()

pygame.quit()
sys.exit()
