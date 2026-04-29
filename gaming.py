from datetime import datetime
from Connect4 import *
from TicTacToe import *
from Othello import *
from Catan import *
import os
import matplotlib.pyplot as plt
import csv
import sys
import time


class Game:
    def __init__(self, index):
        games = [TicTacToe, Connect4, Othello, Catan]
        names = ["TicTacToe", " Connect4", "    Othello", "      Catan", "Bazinga"]
        self.name = names[index]
        self.game = games[index]


class FirstUI:
    def __init__(self, player1, player2, screen):
        self.player1 = player1
        self.player2 = player2
        self.screen = screen

    def run(self):
        background = pygame.image.load("MCA Background.png")
        pygame.display.set_caption("Shabam")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 30)
        text = font.render(self.player1, False, (255, 255, 255))
        text.set_alpha(150)
        self.screen.blit(text, (70, 43))
        text = font.render(self.player2, False, (255, 255, 255))
        text.set_alpha(150)
        self.screen.blit(text, (725, 43))
        t = pygame.Surface((150, 150), pygame.SRCALPHA)
        pygame.draw.rect(t, (255, 255, 255, 150), (0, 0, 130, 130), 4, border_radius=5)
        for x in range(210, 750, 145):
            self.screen.blit(t, (x, 390))
        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x in range(172, 172 + 215) and y in range(305, 305 + 55):
                        leaderBoard = LEADERBOARD(self.player1, self.player2, self.screen)
                        leaderBoard.run()
                    elif x in range(387, 387 + 120) and y in range(305, 305 + 55):
                        stats = STATS(self.player1, self.player2, self.screen)
                        stats.run()
                    elif x in range(507, 507 + 187) and y in range(305, 305 + 55):
                        htp = HTP(self.player1, self.player2, self.screen)
                        htp.run()
                    elif x in range(694, 694 + 147) and y in range(305, 305 + 55):
                        settings = SETTINGS(self.screen, self.player1, self.player2)
                        settings.run()
                    elif y in range(390, 520):
                        if ((x - 210) % 145) < 130 and x < 750:
                            n = ((x - 210) // 145)
                            gameselected = GameSelected(self.player1, self.player2, n, self.screen)
                            gameselected.run()


class GameSelected:
    def __init__(self, player1, player2, gameidx, screen):
        self.player1 = player1
        self.player2 = player2
        self.gameidx = gameidx
        self.screen = screen

    def run(self):
        game = Game(self.gameidx)
        gamename = game.name
        game = game.game
        background = pygame.image.load("SurrondedByGhosts.png")
        pygame.display.set_caption("Shabam")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 55)
        text = font.render(gamename, False, (255, 255, 255))
        text.set_alpha(150)
        self.screen.blit(text, (315, 25))
        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    mode = -1
                    if x in range(300, 585) and y in range(445, 485):
                        mode = 0
                    elif x in range(590, 700) and y in range(445, 485):
                        mode = 1
                    elif x in range(300, 700) and y in range(510, 550):
                        mode = 2
                    elif x in range(300, 700) and y in range(575, 620):
                        mode = 3
                    elif x in range(300, 700) and y in range(640, 685):
                        firstui = FirstUI(self.player1, self.player2, self.screen)
                        firstui.run()
                    if mode in {0, 1, 2, 3}:
                        movearray = []
                        game = game(self.player1, self.player2, mode, self.screen, GameSelected, Resign, CommonWC,
                                    Pause, movearray)
                        game.run()


class Resign:
    def __init__(self, player1, player2, board, screen, mode, whowon, movearray, gameidx, turn, t1, t2, last_tick):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.screen = screen
        self.mode = mode
        self.whowon = whowon
        self.movearray = movearray
        self.gameidx = gameidx
        self.turn = turn
        self.t1 = t1
        self.t2 = t2
        self.last_tick = last_tick

    def run(self):
        background = pygame.image.load("ResignCat.png")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        running = True
        while running:
            presenttime = time.time()
            dt = presenttime - self.last_tick
            self.last_tick = presenttime
            if self.mode == 1:
                if self.turn == 1:
                    self.t1 -= dt
                else:
                    self.t2 -= dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x in range(390, 605) and y in range(545, 595):
                        self.movearray.append((0, "Resigned", 0))
                        commonwc = CommonWC(self.player1, self.player2, self.whowon, self.mode, self.screen,
                                            self.movearray, self.gameidx)
                        commonwc.run()
                    elif x in range(395, 605) and y in range(620, 670):
                        game = Game(self.gameidx).game
                        game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign, CommonWC,
                                    Pause, self.movearray,  t1=self.t1, t2=self.t2,turn=self.turn,board=self.board, last_tick=self.last_tick)
                        game.run()


class CommonWC:
    def __init__(self, player1, player2, whowon, mode, screen, movearray, gameidx,t1=None,t2=None):
        self.player1 = player1
        self.player2 = player2
        self.whowon = whowon
        self.screen = screen
        self.mode = mode
        self.movearray = movearray
        self.gameidx = gameidx
        self.t1 = t1
        self.t2 = t2

    def run(self):
        if self.mode in {0, 1}:
            updatecsv = UpdateCSV(self.player1, self.player2, self.gameidx, self.whowon)
            updatecsv.run()
            if self.gameidx==0:
                os.system("bash leaderboard.sh TicTacToe wins &")
            elif self.gameidx==1:
                os.system("bash leaderboard.sh Connect4 wins &")
            elif self.gameidx==2:
                os.system("bash leaderboard.sh Othello wins &")
        if self.whowon != 0:
            background = pygame.image.load("WinnerFace.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            if self.whowon == 1:
                font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 60)
                text = font.render(self.player1, False, (255, 255, 255))
                self.screen.blit(text, (390, 440))
                pygame.draw.rect(self.screen, (255, 255, 0), (223, 523, 137, 57), 4, 18)
                pygame.display.flip()
            elif self.whowon == 2:
                font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 60)
                text = font.render(self.player2, False, (255, 255, 255))
                self.screen.blit(text, (390, 440))
                pygame.draw.rect(self.screen, (255, 255, 0), (223, 523, 137, 57), 4, 18)
                pygame.display.flip()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(223, 360) and y in range(523, 578):
                            self.movearray = [(datetime.now().replace(microsecond=0), Game(self.gameidx).name,
                                               self.player1, self.player2)] + self.movearray
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                            self.screen.blit(background, (0, 0))
                            self.screen.blit(text, (390, 440))
                            pygame.display.flip()
                        elif x in range(372, 503) and y in range(523, 576):
                            game = STATS(self.player1, self.player2, self.screen, self.gameidx)
                            game.run()
                        elif x in range(517, 673) and y in range(523, 576):
                            game = Game(self.gameidx).game
                            if self.mode in {0,2}:
                                game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign, CommonWC, Pause, self.movearray, turn=1)
                                game.run()
                            if self.mode == 1.1:
                                selected_time = 5
                            elif self.mode == 1.2:
                                selected_time = 10
                            elif self.mode == 1.3:
                                selected_time = 15
                            elif self.mode == 1.4:
                                selected_time = 20
                            elif self.mode == 1.5:
                                selected_time = 30
                            seconds = selected_time * 60
                            game = game(self.player1,self.player2,self.mode,self.screen,GameSelected,Resign,CommonWC,Pause,self.movearray,t1=seconds,t2=seconds,turn=1,last_tick=time.time())
                            game.run()
                        elif x in range(686, 819) and y in range(523, 576):
                            gameselected = GameSelected(self.player1, self.player2, self.gameidx, self.screen)
                            gameselected.run()
        elif self.whowon == 0:
            background = pygame.image.load("ItsaDraw.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 0), (338, 575, 218, 68), 4, 20)
            pygame.display.flip()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(150, 315) and y in range(575, 640):
                            game = Game(self.gameidx).game
                            if self.mode in {0,2}:
                                game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign, CommonWC, Pause, self.movearray, turn=1)
                                game.run()
                            elif self.mode == 1.1:
                                selected_time = 5
                            elif self.mode == 1.2:
                                selected_time = 10
                            elif self.mode == 1.3:
                                selected_time = 15
                            elif self.mode == 1.4:
                                selected_time = 20
                            elif self.mode == 1.5:
                                selected_time = 30
                            seconds = selected_time * 60
                            game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign,
                                        CommonWC, Pause, self.movearray,t1=seconds,t2=seconds,turn=1,last_tick=time.time())
                            game.run()
                        elif x in range(340, 555) and y in range(575, 640):
                            self.movearray = [(datetime.now().replace(microsecond=0), Game(self.gameidx).name,
                                               self.player1, self.player2)] + self.movearray
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                            self.screen.blit(background, (0, 0))
                            pygame.display.flip()
                        elif x in range(575, 710) and y in range(575, 640):
                            STATS(self.player1, self.player2, self.screen, self.gameidx)
                        elif x in range(735, 865) and y in range(575, 640):
                            gameselected = GameSelected(self.player1, self.player2, self.gameidx, self.screen)
                            gameselected.run()


class UpdateCSV:
    def __init__(self, player1, player2, game, result):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.result = result

    def run(self):
        Time = datetime.now().replace(microsecond=0, second=0)
        with open("Serial.txt", "r", newline="") as Sno:
            Sno = int(Sno.read())
            Sno += 1
        with open("Serial.txt", "w") as NewSno:
            NewSno.write(str(Sno))
        with open("history.csv", "a", newline="") as history:
            append = csv.writer(history)
            append.writerow([Sno, Time, self.game, self.player1, self.player2, self.result])


class Pause:
    def __init__(self, player1, player2, board, screen, mode, movearray, gameidx, turn, t1, t2):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.screen = screen
        self.mode = mode
        self.movearray = movearray
        self.gameidx = gameidx
        self.turn = turn
        self.t1 = t1
        self.t2 = t2

    def run(self):
        background = pygame.image.load("PausedScreen.png")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x in range(375, 620) and y in range(470, 540):
                        game = Game(self.gameidx).game
                        game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign, CommonWC,Pause, self.movearray,  t1=self.t1, t2=self.t2,turn=self.turn,board=self.board,last_tick=time.time())
                        game.run()
                    elif x in range(240, 480) and y in range(560, 630):
                        game = Game(self.gameidx).game
                        if self.mode in {0, 2}:
                            game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign,CommonWC, Pause, self.movearray, turn=1)
                            game.run()
                        if self.mode == 1.1:
                            selected_time = 5
                        elif self.mode == 1.2:
                            selected_time = 10
                        elif self.mode == 1.3:
                            selected_time = 15
                        elif self.mode == 1.4:
                            selected_time = 20
                        elif self.mode == 1.5:
                            selected_time = 30
                        seconds = selected_time * 60
                        game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign, CommonWC,Pause, self.movearray,t1=seconds,t2=seconds,turn=1,last_tick=time.time())
                        game.run()
                    elif x in range(515, 760) and y in range(565, 630):
                        gameselected = GameSelected(self.player1, self.player2, self.gameidx, self.screen)
                        gameselected.run()


def compute_leaderboard(sort_by="wins", game_filter=None):
    valid_sorts = {"wins", "losses", "ratio", "rating"}

    if sort_by not in valid_sorts:
        sort_by = "wins"

    stats = {}

    with open("history.csv", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            game = row["Game"]
            p1 = row["Player 1"]
            p2 = row["Player 2"]
            result = int(row["Result"])

            if game_filter and game != game_filter:
                continue

            if game_filter is None:
                key1 = p1
                key2 = p2
            else:
                key1 = (game, p1)
                key2 = (game, p2)

            stats.setdefault(key1, {"wins": 0.0, "losses": 0.0})
            stats.setdefault(key2, {"wins": 0.0, "losses": 0.0})

            if result == 1:
                stats[key1]["wins"] += 1
                stats[key2]["losses"] += 1
            elif result == 2:
                stats[key2]["wins"] += 1
                stats[key1]["losses"] += 1
            elif result == 0:
                stats[key1]["wins"] += 0.5
                stats[key2]["wins"] += 0.5
                stats[key1]["losses"] += 0.5
                stats[key2]["losses"] += 0.5

    leaderboard = []

    for key, val in stats.items():
        if game_filter is None:
            player = key
            game = "Overall"
        else:
            game, player = key

        w = val["wins"]
        l = val["losses"]
        ratio = float("inf") if l == 0 else w / l

        leaderboard.append({
            "game": game,
            "player": player,
            "wins": w,
            "losses": l,
            "ratio": ratio
        })

    # Sorting the leaderboard based on the specified criteria
    if sort_by == "wins":
        leaderboard.sort(key=lambda x: (x["wins"], x["ratio"]), reverse=True)
    elif sort_by == "losses":
        leaderboard.sort(key=lambda x: (x["losses"], x["wins"]), reverse=True)
    elif sort_by == "ratio":
        leaderboard.sort(key=lambda x: (x["ratio"], x["wins"]), reverse=True)
    elif sort_by == "rating":
        leaderboard.sort(key=lambda x: (x["wins"] * 10), reverse=True)

    return leaderboard


class LEADERBOARD:
    def __init__(self, player1, player2, screen):
        self.player1 = player1
        self.player2 = player2
        self.screen = screen

    def run(self):
        background = pygame.image.load("Leaderboard.png")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (150, 230, 280, 280), width=4)
        for x in (0, 1):
            for y in (0, 1):
                pygame.draw.rect(self.screen, (255, 255, 255), (520 + 147.5 * x, 230 + 147.5 * y, 130, 130), width=4)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    background = pygame.image.load("Leaderboardprint.png")
                    background = pygame.transform.scale(background, (1000, 700))

                    if (x - 147) ** 2 + (y - 143) ** 2 < 2025:
                        game = FirstUI(self.player1, self.player2, self.screen)
                        game.run()

                    elif x in range(150, 430) and y in range(230, 510):
                        os.system("bash leaderboard.sh Overall wins &")
                        self.screen.blit(background, (0, 0))
                        pygame.display.flip()
                        self.show(None)

                    elif x in range(520, 650) and y in range(230, 360):
                        os.system("bash leaderboard.sh TicTacToe wins &")
                        self.screen.blit(background, (0, 0))
                        pygame.display.flip()
                        self.show("TicTacToe")

                    elif x in range(670, 800) and y in range(230, 360):
                        os.system("bash leaderboard.sh Connect4 wins &")
                        self.screen.blit(background, (0, 0))
                        pygame.display.flip()
                        self.show("Connect4")

                    elif x in range(520, 650) and y in range(380, 510):
                        os.system("bash leaderboard.sh Othello wins &")
                        self.screen.blit(background, (0, 0))
                        pygame.display.flip()
                        self.show("Othello")

                    elif x in range(670, 800) and y in range(380, 510):
                        os.system("bash leaderboard.sh Catan wins &")
                        self.screen.blit(background, (0, 0))
                        pygame.display.flip()
                        self.show("Catan")

    def show(self, game_filter, sortidx=0):
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 18)

        sort_options = ["wins", "losses", "ratio", "rating"]

        while True:
            background = pygame.image.load("Leaderboardprint.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))

            data = compute_leaderboard(sort_options[sortidx], game_filter)
            y = 275
            row_height = 38

            for i, row in enumerate(data[:10]):
                ratio = "∞" if row["ratio"] == float("inf") else f"{row['ratio']:.2f}"
                rating = int(row["wins"] * 10)

                self.screen.blit(font.render(row["player"], True, (255, 255, 255)), (200, y))
                self.screen.blit(font.render(str(int(row["wins"])), True, (255, 255, 255)), (410, y))
                self.screen.blit(font.render(str(int(row["losses"])), True, (255, 255, 255)), (530, y))
                self.screen.blit(font.render(ratio, True, (255, 255, 255)), (650, y))
                self.screen.blit(font.render(str(rating), True, (255, 255, 255)), (800, y))

                y += row_height

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if (x - 57) ** 2 + (y - 57) ** 2 < 1600:
                        game = LEADERBOARD(self.player1, self.player2, self.screen)
                        game.run()

                    elif x in range(840, 980) and y in range(110, 150):
                        self.show(game_filter, (sortidx + 1) % 4)


class HTP:
    def __init__(self, player1, player2, screen):
        self.player1 = player1
        self.player2 = player2
        self.screen = screen

    def run(self):
        background = pygame.image.load("HTP.png")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        for x in (0, 1):
            for y in (0, 1):
                pygame.draw.rect(self.screen, (255, 255, 255), (160 + 500 * x, 180 + 200 * y, 180, 180), 4)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if (x in range(160, 340) or x in range(660, 840)) and (
                            y in range(180, 360) or y in range(380, 560)):
                        self.show_instructions((x - 160) // 500 + (y - 180) // 100)
                    elif x in range(28, 215) and y in range(28, 90):
                        game = FirstUI(self.player1, self.player2, self.screen)
                        game.run()

    def show_instructions(self, gameidx):
        background = pygame.image.load("HowToPlay.png")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))

        game = Game(gameidx).name.strip()

        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 20)
        title_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 70)
        title_text = title_font.render(game, True, (255, 255, 255))
        self.screen.blit(title_text, (300, 40))
        instructions = {
            "TicTacToe": [
                "• Played on a 10 × 10 grid",
                "• Two players take turns placing their mark (X or O)",
                "• A move can be made on any empty cell",
                "• The objective is to get 5 of your marks in a row",
                "• Valid lines: horizontal, vertical, or diagonal",
                "• Blocking your opponent is just as important as attacking",
                "• The game ends when a player gets 5 in a row",
                "• If the board fills with no winner, the game is a draw"
            ],

            "Connect4": [
                "• Played on a 7 × 7 vertical board",
                "• Players take turns choosing a column to drop their piece",
                "• Pieces fall to the lowest available space in that column",
                "• You cannot place a piece in a full column",
                "• The goal is to connect 4 of your pieces in a row",
                "• Valid lines: horizontal, vertical, or diagonal",
                "• Plan ahead—stacking can create multiple threats",
                "• Game ends when a player connects 4 or the board fills"
            ],

            "Othello": [
                "• Played on an 8 × 8 board with two colors",
                "• Players take turns placing a piece on the board",
                "• A valid move must capture at least one opponent piece",
                "• Capture occurs by surrounding opponent pieces in a straight line",
                "• All captured pieces flip to your color",
                "• You must play a move if one is available",
                "• If no moves are available, your turn is skipped",
                "• The game ends when neither player can move",
                "• The player with the most pieces on the board wins"
            ],

            "Catan": [
                "• Follows standard Settlers of Catan rules",
                "• Players collect resources: wood, brick, sheep, wheat, ore",
                "• Resources are gained based on dice rolls and tile numbers",
                "• Build roads to expand and connect settlements",
                "• Upgrade settlements into cities for more resource gain",
                "• Trade resources with players or the bank",
                "• Strategic placement at the start is very important",
                "• Development cards provide special advantages",
                "• First player to reach the required victory points wins"
            ]
        }
        lines = instructions.get(game, ["No instructions available"])

        y = 150
        for line in lines:
            text = font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (100, y))
            y += 28

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if (x - 47) ** 2 + (y - 51) ** 2 < 1000:
                        game = HTP(self.player1, self.player2, self.screen)
                        game.run()
                        return


class SETTINGS:
    def __init__(self, screen, player1, player2):
        self.screen = screen
        self.player1 = player1
        self.player2 = player2

    def run(self):
        background = pygame.image.load("Settings.png")
        background = pygame.transform.scale(background, (1000, 700))
        running = True
        while running:
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if 340 <= x <= 677 and 310 <= y <= 382:
                        pygame.quit()

                    elif 340 <= x <= 677 and 408 <= y <= 475:
                        os.system('cmd.exe /c start https://mail.google.com/mail/?view=cm&to=email2rajit@gmail.com')

                    elif 340 <= x <= 676 and 501 <= y <= 568:
                        game = FirstUI(self.player1, self.player2, self.screen)
                        game.run()


class STATS:
    def __init__(self, player1, player2, screen, idx=None):
        self.player1 = player1
        self.player2 = player2
        self.screen = screen
        self.idx = idx

    def run(self):
        self.generate_graphs()
        self.display_graphs()

    def load_data(self):
        from collections import defaultdict, Counter
        wins = defaultdict(int)
        games = []
        with open("history.csv", newline="") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                p1 = row[3]
                p2 = row[4]
                result = int(row[5])
                game = row[2]
                games.append(game)
                if result == 1:
                    wins[p1] += 1
                elif result == 2:
                    wins[p2] += 1
                elif result == 0:
                    wins[p1] += 0.5
                    wins[p2] += 0.5
        return wins, Counter(games)

    def generate_graphs(self):
        wins, game_counts = self.load_data()
        top = sorted(wins.items(), key=lambda x: x[1], reverse=True)[:5]
        players = [x[0] for x in top]
        win_counts = [x[1] for x in top]
        plt.figure()
        plt.bar(players, win_counts)
        plt.title("Top 5 Players")
        plt.xlabel("Players")
        plt.ylabel("Wins")
        plt.savefig("top_players.png")
        plt.close()
        labels = list(game_counts.keys())
        sizes = list(game_counts.values())
        plt.figure()
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title("Game Popularity")
        plt.savefig("game_popularity.png")
        plt.close()

    def display_graphs(self):
        img1 = pygame.image.load("top_players.png")
        img2 = pygame.image.load("game_popularity.png")
        img1 = pygame.transform.scale(img1, (500, 500))
        img2 = pygame.transform.scale(img2, (500, 375))
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 25)
        while True:
            self.screen.fill((255, 255, 255))
            self.screen.blit(img2, (500, 200))
            self.screen.blit(img1, (100, 100))
            pygame.draw.rect(self.screen, (0, 0, 0), (50, 50, 150, 40), 0, 20)
            text = font.render("Back", True, (255, 255, 255))
            self.screen.blit(text, (75, 55))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x in range(50, 200) and y in range(50, 90):
                        if self.idx is None:
                            game = FirstUI(self.player1, self.player2, self.screen)
                            game.run()
                        else:
                            game=GameSelected(self.player1, self.player2,self.idx, self.screen)
                            game.run()

clock = pygame.time.Clock()
clock.tick(60)
pygame.init()
Bigscreen = pygame.display.set_mode((1000, 700))
Biggame = FirstUI(str(sys.argv[1]), str(sys.argv[2]), Bigscreen)
Biggame.run()
pygame.quit()
