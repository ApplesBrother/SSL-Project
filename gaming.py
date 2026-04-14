from datetime import datetime
from Connect4 import *
import csv

class Game:
    def __init__(self,index):
        names=["TicTacToe"," Connect4","    Othello","      Chess","Bazinga"]
        self.name=names[index]


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
                            game=TicTacToe(self.player1,self.player2,mode,self.screen)
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
                        game=Connect4(self.player1,self.player2,self.mode,self.screen, GameSelected, Resign, CommonWC,UpdateCSV, self.movearray)
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
                        x, y = pygame.mouse.get_pos()
                        if x in range(210, 380) and y in range(565, 630):
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                        elif x in range(415, 600) and y in range(565, 630):
                            game = Connect4(self.player1, self.player2, self.mode, self.screen,GameSelected, Resign, CommonWC,UpdateCSV, self.movearray)
                            game.run()
                        elif x in range(630, 810) and y in range(565, 630):
                            game = GameSelected(self.player1, self.player2, 1, self.screen)
                            game.run()
        elif self.whowon==0:
            background = pygame.image.load("ItsaDraw.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            pygame.display.flip()
            running=True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(220,390) and y in range(575,640):
                            game = Connect4(self.player1, self.player2, self.mode, self.screen, GameSelected,Resign,CommonWC,UpdateCSV, self.movearray)
                            game.run()
                        elif x in range(420,625) and y in range(575,640):
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                        elif x in range(650,800) and y in range(575,640):
                            game = GameSelected(self.player1, self.player2, 1, self.screen)
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

pygame.init()
Bigscreen=pygame.display.set_mode((1000,700))
Biggame=FirstUI("Kavya","Rajit",Bigscreen)
Biggame.run()
