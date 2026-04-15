from datetime import datetime
from Connect4 import *
from TicTacToe import *
from Othello import *
import csv

class Game:
    def __init__(self,index):
        names=["TicTacToe"," Connect4","    Othello","      Chess","Bazinga"]
        self.name=names[index]

GAME_MAP = {"TicTacToe": 0,"Connect4": 1,"Othello": 2,"Chess": 3,"Bazinga": 4}

def start_game(player1, player2, game_name, mode, screen):
    movearray = []
    if game_name == "TicTacToe":
        game = TicTacToe(player1, player2, mode, screen, GameSelected, Resign, CommonWC, UpdateCSV, movearray)
    elif game_name == "Connect4":
        game = Connect4(player1, player2, mode, screen, GameSelected, Resign, CommonWC, UpdateCSV, movearray)
    elif game_name == "Othello":
        game = Othello(player1, player2, mode, screen)
    elif game_name == "Chess":
        game = Chess(player1, player2, mode, screen)
    elif game_name == "Bazinga":
        game = Bazinga(player1, player2, mode, screen)

    game.run()

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
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf",30)
        text=font.render(self.player1, False, (255, 255, 255))
        text.set_alpha(150)
        self.screen.blit(text, (70, 43))
        text=font.render(self.player2, False, (255, 255, 255))
        text.set_alpha(150)
        self.screen.blit(text, (725, 43))
        t = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(t,(255, 255, 255, 150),(0, 0, 100, 100),4,border_radius=5)
        for x in range(210,800,120):
            self.screen.blit(t, (x, 390))
        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x in range(172, 172 + 215) and y in range(305, 305 + 55):
                        leaderBoard=LEADERBOARD(self.player1,self.player2,self.screen)
                        leaderBoard.run()
                    elif x in range(387, 387 + 120) and y in range(305, 305 + 55):
                        stats=STATS(self.player1,self.player2)
                        stats.run()
                    elif x in range(507, 507 + 187) and y in range(305, 305 + 55):
                        htp=HTP()
                        htp.run()
                    elif x in range(694, 694 + 147) and y in range(305, 305 + 55):
                        settings=SETTINGS(self.player1,self.player2)
                        settings.run()
                    elif y in range(390,491):
                        if ((x-210)%120)<100 and x<790:
                            n=((x-210)//120)
                            game=GameSelected(self.player1,self.player2,n,self.screen)
                            game.run()
        pygame.quit()

class GameSelected:
    def __init__(self, player1, player2, game, screen):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.screen = screen

    def run(self):
        pygame.init()
        game=Game(self.game)
        background = pygame.image.load("SurrondedByGhosts.png")
        pygame.display.set_caption("Shabam")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 55)
        text = font.render(game.name, False, (255, 255, 255))
        text.set_alpha(150)
        self.screen.blit(text, (315, 25))
        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    mode = -1
                    if x in range(300,585) and y in range(445,485):
                        mode=0
                    elif x in range(590,700) and y in range(445,485):
                        mode=1
                    elif x in range(300,700) and y in range(510,550):
                        mode=2
                    elif x in range(300,700) and y in range(575,620):
                        mode=3
                    elif x in range(300,700) and y in range(640,685):
                        game=FirstUI(self.player1,self.player2,self.screen)
                        game.run()
                    if mode in {0,1,2,3}:
                        movearray=[]
                        if self.game==0:
                            game=TicTacToe(self.player1,self.player2,mode,self.screen,GameSelected,Resign,CommonWC,UpdateCSV,movearray)
                        elif self.game==1:
                            game=Connect4(self.player1,self.player2,mode,self.screen,GameSelected,Resign,CommonWC,UpdateCSV,movearray)
                        elif self.game==2:
                            game=Othello(self.player1,self.player2,mode,self.screen)
                        elif self.game==3:
                            game=Chess(self.player1,self.player2,mode,self.screen)
                        else:
                            game=Bazinga(self.player1,self.player2,mode,self.screen)
                        game.run()
        pygame.quit()

class Resign:
    def __init__(self,player1,player2,board,screen,mode,whowon, movearray):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.screen = screen
        self.mode=mode
        self.whowon=whowon
        self.movearray = movearray
    def run(self):
        background = pygame.image.load("ResignCat.png")
        background = pygame.transform.scale(background, (1000, 700))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        running=True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x in range(390, 605) and y in range(545, 595):
                        self.movearray.append((0,"Resigned",0))
                        game=UpdateCSV(self.player1,self.player2,self.movearray[0][1],self.whowon)
                        game.run()
                        game = CommonWC(self.player1, self.player2, self.whowon, self.mode ,self.screen,self.movearray)
                        game.run()
                    elif x in range(395, 605) and y in range(620, 670):
                        game_name = self.movearray[0][1]
                        start_game(self.player1, self.player2, game_name, self.mode, self.screen)

class CommonWC:
    def __init__(self,player1,player2,whowon,mode,screen,movearray):
        self.player1 = player1
        self.player2 = player2
        self.whowon=whowon
        self.screen = screen
        self.mode=mode
        self.movearray = movearray

    def run(self):
        if self.whowon!=0:
            background = pygame.image.load("WinnerFace.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            if self.whowon==1:
                font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 60)
                text = font.render(self.player1, False, (255, 255, 255))
                self.screen.blit(text, (390, 460))
                pygame.display.flip()
            elif self.whowon==2:
                font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 60)
                text = font.render(self.player2, False, (255, 255, 255))
                self.screen.blit(text, (390, 460))
                pygame.display.flip()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(210, 380) and y in range(565, 630):
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                            dfont=pygame.font.Font(None, 60)
                            text=dfont.render("d",False, (255, 255, 255))
                            self.screen.blit(text, (330, 580))
                            pygame.display.flip()
                        elif x in range(415, 600) and y in range(565, 630):
                            game_name = self.movearray[0][1]
                            start_game(self.player1, self.player2, game_name, self.mode, self.screen)

                        elif x in range(630, 810) and y in range(565, 630):
                            game_name = self.movearray[0][1]
                            game_index = GAME_MAP[game_name]

                            game = GameSelected(self.player1, self.player2, game_index, self.screen)
                            game.run()
        elif self.whowon==0:
            background = pygame.image.load("ItsaDraw.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 0), (415, 575, 215, 68), 4, 20)
            pygame.display.flip()
            running=True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(220,390) and y in range(575,640):
                            game_name = self.movearray[0][1]
                            start_game(self.player1, self.player2, game_name, self.mode, self.screen)

                        elif x in range(420,625) and y in range(575,640):
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                            self.screen.blit(background, (0, 0))
                            pygame.display.flip()
                        elif x in range(650,800) and y in range(575,640):
                            game_name = self.movearray[0][1]
                            game_index = GAME_MAP[game_name]

                            game = GameSelected(self.player1, self.player2, game_index, self.screen)
                            game.run()

class UpdateCSV:
    def __init__(self,player1,player2,game,result):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.result = result

    def run(self):
        Time = datetime.now().replace(microsecond=0)
        with open("Serial.txt", "r", newline="") as Sno:
            Sno = int(Sno.read())
            Sno += 1
        with open("Serial.txt", "w") as NewSno:
            NewSno.write(str(Sno))
        with open("history.csv", "a",newline="") as history:
            append = csv.writer(history)
            append.writerow([Sno, Time,self.game, self.player1, self.player2, self.result])

def compute_leaderboard(sort_by="wins", game_filter=None):
    valid_sorts = {"wins", "losses", "ratio"}

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
    
    return leaderboard

class LEADERBOARD:
    def __init__(self,player1,player2,screen):
        self.player1 = player1
        self.player2 = player2
        self.screen = screen

    def run(self):
        previous_screen = self.screen.copy()
        background = pygame.image.load("LEADERBOARD.png")
        background = pygame.transform.scale(background, (1000, 700))

        title_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 50)
        label_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 30)
        back_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 20)

        overall_img = pygame.image.load("overall.png").convert_alpha()
        ttt_img = pygame.image.load("ttt.png").convert_alpha()
        c4_img = pygame.image.load("c4.png").convert_alpha()
        othello_img = pygame.image.load("othello.png").convert_alpha()

        overall_img = pygame.transform.scale(overall_img, (400, 200))
        ttt_img = pygame.transform.scale(ttt_img, (400, 200))
        c4_img = pygame.transform.scale(c4_img, (400, 200))
        othello_img = pygame.transform.scale(othello_img, (400, 200))

        overall_rect = overall_img.get_rect(topleft=(75, 100))
        ttt_rect = ttt_img.get_rect(topleft=(525, 100))
        c4_rect = c4_img.get_rect(topleft=(75, 400))
        othello_rect = othello_img.get_rect(topleft=(525, 400))
        back_rect = pygame.Rect(20, 20, 100, 30)

        while True:
            self.screen.blit(background, (0, 0))

            title = title_font.render("LEADERBOARD", True, (255, 255, 255))
            self.screen.blit(title, (250, 20))

            self.screen.blit(overall_img, overall_rect)
            self.screen.blit(ttt_img, ttt_rect)
            self.screen.blit(c4_img, c4_rect)  
            self.screen.blit(othello_img, othello_rect)

            self.screen.blit(label_font.render("Overall", True, (255, 255, 255)), (overall_rect.x + 120, overall_rect.y + 210)) 
            self.screen.blit(label_font.render("TicTacToe", True, (255, 255, 255)), (ttt_rect.x + 100, ttt_rect.y + 210))
            self.screen.blit(label_font.render("Connect4", True, (255, 255, 255)), (c4_rect.x + 100, c4_rect.y + 210))
            self.screen.blit(label_font.render("Othello", True, (255, 255, 255)), (othello_rect.x + 130, othello_rect.y + 210))

            pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 2)
            back_text = back_font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 5))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if back_rect.collidepoint(x, y):
                        self.screen.blit(previous_screen, (0, 0))
                        pygame.display.flip()
                        return
                    
                    if overall_rect.collidepoint(x, y):
                        self.show(None)
                    elif ttt_rect.collidepoint(x, y):
                        self.show("TicTacToe")
                    elif c4_rect.collidepoint(x, y):
                        self.show("Connect4")
                    elif othello_rect.collidepoint(x, y):
                        self.show("Othello")
            
    def show(self, game_filter):
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 18)
        title_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 40)
        back_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 20)

        if game_filter is None:
            title_text = "OVERALL"
        else:
            title_text = f"{game_filter}"

        sort_options = ["wins", "losses", "ratio"]
        selected_sort = "wins"
        dropdown_open = False

        dropdown_rect = pygame.Rect(750, 20, 200, 30)
        back_rect = pygame.Rect(20, 20, 100, 30)

        x_player = 80
        x_wins = 300
        x_losses = 450
        x_ratio = 600

        while True:
            self.screen.fill((0, 0, 0))

            pygame.draw.rect(self.screen, (255, 255, 255), dropdown_rect, 2)
            text = font.render(f"Sort by: {selected_sort}", True, (255, 255, 255))
            self.screen.blit(text, (dropdown_rect.x + 5, dropdown_rect.y + 5))

            pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 2)
            back_text = back_font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 5))

            if dropdown_open:
                for i, option in enumerate(sort_options):
                    option_rect = pygame.Rect(750, 50 + i * 30, 200, 30)
                    pygame.draw.rect(self.screen, (255, 255, 255), option_rect, 1)

                    option_text = font.render(option.capitalize(), True, (255, 255, 255))
                    self.screen.blit(option_text, (option_rect.x + 5, option_rect.y + 5))
            
            title_surface = title_font.render(title_text, True, (255, 255, 255))
            self.screen.blit(title_surface, (250, 20))

            data = compute_leaderboard(selected_sort, game_filter)

            y = 80
            self.screen.blit(font.render("Player", True, (255, 255, 255)), (x_player, y))
            self.screen.blit(font.render("Wins", True, (255, 255, 255)), (x_wins, y))
            self.screen.blit(font.render("Losses", True, (255, 255, 255)), (x_losses, y))
            self.screen.blit(font.render("Ratio", True, (255, 255, 255)), (x_ratio, y))
            y += 30

            pygame.draw.line(self.screen, (255, 255, 255), (280, 80), (280, 600))
            pygame.draw.line(self.screen, (255, 255, 255), (430, 80), (430, 600))
            pygame.draw.line(self.screen, (255, 255, 255), (580, 80), (580, 600))

            for row in data:
                ratio = "∞" if row["ratio"] == float("inf") else f"{row['ratio']:.2f}"

                self.screen.blit(font.render(row["player"], True, (255, 255, 255)), (x_player, y))
                self.screen.blit(font.render(str(int(row["wins"])), True, (255, 255, 255)), (x_wins, y))
                self.screen.blit(font.render(str(int(row["losses"])), True, (255, 255, 255)), (x_losses, y))
                self.screen.blit(font.render(ratio, True, (255, 255, 255)), (x_ratio, y))
                y += 25

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if dropdown_rect.collidepoint(x, y):
                        dropdown_open = not dropdown_open
                    elif dropdown_open:
                        for i, option in enumerate(sort_options):
                            option_rect = pygame.Rect(750, 50 + i * 30, 200, 30)
                            if option_rect.collidepoint(x, y):
                                selected_sort = option
                                dropdown_open = False
                                break
                    elif back_rect.collidepoint(x, y):
                        return

class HTP:
    def __init__(self):
        pass

    def run(self):
        background = pygame.image.load("LEADERBOARD.png")
        background = pygame.transform.scale(background, (1000, 700))
        
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 40)
        label_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 25)

        ttt_img = pygame.image.load("ttt.png").convert_alpha()
        c4_img = pygame.image.load("c4.png").convert_alpha()
        othello_img = pygame.image.load("othello.png").convert_alpha()

        ttt_img = pygame.transform.scale(ttt_img, (400, 200))
        c4_img = pygame.transform.scale(c4_img, (400, 200))
        othello_img = pygame.transform.scale(othello_img, (400, 200))

        ttt_rect = ttt_img.get_rect(topleft=(75, 150))
        c4_rect = c4_img.get_rect(topleft=(525, 150))
        othello_rect = othello_img.get_rect(topleft=(300, 400))
        back_rect = pygame.Rect(20, 20, 100, 30)

        screen = pygame.display.get_surface()
        previous_screen = screen.copy()

        while True:
            screen.blit(background, (0, 0))

            title = font.render("How To Play", True, (255, 255, 255))
            screen.blit(title, (300, 20))

            screen.blit(ttt_img, ttt_rect)
            screen.blit(c4_img, c4_rect)  
            screen.blit(othello_img, othello_rect)

            screen.blit(label_font.render("TicTacToe", True, (255, 255, 255)), (ttt_rect.x + 120, ttt_rect.y + 210)) 
            screen.blit(label_font.render("Connect4", True, (255, 255, 255)), (c4_rect.x + 100, c4_rect.y + 210))
            screen.blit(label_font.render("Othello", True, (255, 255, 255)), (othello_rect.x + 130, othello_rect.y + 210))

            pygame.draw.rect(screen, (255, 255, 255), back_rect, 2)
            back_text = label_font.render("Back", True, (255, 255, 255))
            screen.blit(back_text, (back_rect.x + 10, back_rect.y + 5))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if back_rect.collidepoint(x,y):
                        screen.blit(previous_screen, (0, 0))
                        pygame.display.flip()
                        return
                    elif ttt_rect.collidepoint(x,y):
                        self.show_instructions("TicTacToe")
                    elif c4_rect.collidepoint(x,y):
                        self.show_instructions("Connect4")
                    elif othello_rect.collidepoint(x,y):
                        self.show_instructions("Othello")
                    
    def show_instructions(self, game_name):
        screen = pygame.display.get_surface()
        font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 25)
        title_font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 40)

        back_rect = pygame.Rect(20, 20, 100, 30)

        instructions = {
            "TicTacToe": [
                "TicTacToe is a simple game where two players take turns marking spaces in a 3x3 grid.",
                "The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins.",
                "If all spaces are filled and no player has three in a row, the game is a draw."
            ],
            "Connect4": [
                "Connect4 is a two-player connection game where players take turns dropping colored discs into a vertical grid.",
                "The objective is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.",
                "The game ends when one player achieves this or when the board is completely filled, resulting in a draw."
            ],
            "Othello": [
                "Othello is a strategy board game played on an 8x8 grid.",
                "Players take turns placing their pieces on the board, with the goal of capturing their opponent's pieces by surrounding them.",
                "The player with the most pieces on the board at the end of the game wins."
            ]
        }

        lines = instructions[game_name]

        while True:
            screen.fill((0, 0, 0))

            pygame.draw.rect(screen, (255, 255, 255), back_rect, 2)
            screen.blit(font.render("Back", True, (255, 255, 255)), (back_rect.x + 10, back_rect.y + 5))

            title_surface = title_font.render(game_name, True, (255, 255, 255))
            screen.blit(title_surface, (300, 20))

            y = 100

            for line in lines:
                text = font.render(line, True, (255, 255, 255))
                screen.blit(text, (100, y))
                y += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if back_rect.collidepoint(x, y):
                        return

pygame.init()
Bigscreen=pygame.display.set_mode((1000,700))
Biggame=FirstUI("Garv","Rajit",Bigscreen)
Biggame.run()
