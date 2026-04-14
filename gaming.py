from Connect4 import *

class Game:
    def __init__(self,index):
        names=["TicTacToe"," Connect4","    Othello","      Chess","Bazinga"]
        Game.name=names[index]


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
                        leaderBoard=LEADERBOARD(self.player1,self.player2)
                        leaderBoard.run()
                    elif x in range(387, 387 + 120) and y in range(305, 305 + 55):
                        stats=STATS(self.player1,self.player2)
                        stats.run()
                    elif x in range(507, 507 + 187) and y in range(305, 305 + 55):
                        htp=HTP()
                        htp.run
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
                        movearray=np.array([])
                        if self.game==0:
                            game=TicTacToe(self.player1,self.player2,mode,self.screen)
                        elif self.game==1:
                            game=Connect4(self.player1,self.player2,mode,self.screen,GameSelected,Resign,CommonWC,movearray)
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
                    print(pygame.mouse.get_pos())
                    x, y = pygame.mouse.get_pos()
                    if x in range(390, 605) and y in range(545, 595):
                        wincheck = CommonWC(self.player1, self.player2, self.whowon, self.mode ,self.screen,self.movearray)
                        wincheck.run()
                    elif x in range(395, 605) and y in range(620, 670):
                        game=Connect4(self.player1,self.player2,self.mode,self.screen, GameSelected, Resign, CommonWC, self.movearray)
                        game.board=self.board
                        game.run()

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
                        print(pygame.mouse.get_pos())
                        x, y = pygame.mouse.get_pos()
                        if x in range(210, 380) and y in range(565, 630):
                            print("save it")
                        elif x in range(415, 600) and y in range(565, 630):
                            game = Connect4(self.player1, self.player2, self.mode, self.screen,GameSelected, Resign, CommonWC, self.movearray)
                            game.run()
                        elif x in range(630, 810) and y in range(565, 630):
                            game = GameSelected(self.player1, self.player2, 1, self.screen)
                            game.run()
        elif self.whowon==0:
            global draw1, draw2
            draw1=False
            draw2=False
            background = pygame.image.load("ItsaDraw.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            pygame.display.flip()
            running=True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(pygame.mouse.get_pos())
                        x, y = pygame.mouse.get_pos()
                        if x in range(220,390) and y in range(575,640):
                            game = Connect4(self.player1, self.player2, self.mode, self.screen, GameSelected,
                                            self.movearray)
                            game.run()
                        elif x in range(420,625) and y in range(575,640):
                            print("Save it")
                        elif x in range(650,800) and y in range(575,640):
                            game = GameSelected(self.player1, self.player2, 1, self.screen)
                            game.run()
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

pygame.init()
screen=pygame.display.set_mode((1000,700))
game=FirstUI("Kavya","Rajit",screen)
game.run()
