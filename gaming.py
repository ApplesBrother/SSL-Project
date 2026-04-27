from datetime import datetime
from Connect4 import *
'''from TicTacToe import *'''
from Othello import *
from hello import *
import csv
import time
import ast

class Game:
    def __init__(self,index):
        games=[TicTacToe,Connect4,Othello]
        names=["TicTacToe"," Connect4","    Othello","      Chess","Bazinga"]
        self.name=names[index]
        self.game=games[index]

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
                    pygame.quit()
                    return
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
                            gameselected=GameSelected(self.player1,self.player2,n,self.screen)
                            gameselected.run()

class GameSelected:
    def __init__(self, player1, player2, gameidx, screen):
        self.player1 = player1
        self.player2 = player2
        self.gameidx = gameidx
        self.screen = screen

    def run(self):
        game=Game(self.gameidx)
        gamename=game.name
        game=game.game
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
                    return
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
                        firstui=FirstUI(self.player1,self.player2,self.screen)
                        firstui.run()
                    if mode in {0,1,2,3}:
                        movearray=[]
                        game=game(self.player1,self.player2,mode,self.screen,GameSelected,Resign,CommonWC,Pause,movearray)
                        game.run()

class Resign:
    def __init__(self,player1,player2,board,screen,mode,whowon, movearray,gameidx,turn,t1, t2, last_tick):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.screen = screen
        self.mode=mode
        self.whowon=whowon
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
        running=True
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
                    running=False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x in range(390, 605) and y in range(545, 595):
                        self.movearray.append((0,"Resigned",0))
                        commonwc = CommonWC(self.player1, self.player2, self.whowon, self.mode ,self.screen,self.movearray,self.gameidx)
                        commonwc.run()
                    elif x in range(395, 605) and y in range(620, 670):
                        game=Game(self.gameidx).game
                        game = game(self.player1, self.player2,self.mode,self.screen,GameSelected,Resign,CommonWC,Pause, self.movearray, self.turn, self.t1, self.t2, self.last_tick, self.board)
                        game.run()

class CommonWC:
    def __init__(self,player1,player2,whowon,mode,screen,movearray,gameidx):
        self.player1 = player1
        self.player2 = player2
        self.whowon=whowon
        self.screen = screen
        self.mode=mode
        self.movearray = movearray
        self.gameidx = gameidx

    def run(self):
        if self.mode in {0, 1}:
            updatecsv = UpdateCSV(self.player1, self.player2, self.gameidx, self.whowon)
            updatecsv.run()
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
                    if event.type == pygame.QUIT:
                        running=False
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(210, 380) and y in range(565, 630):
                            self.movearray=[(datetime.now().replace(microsecond=0),Game(self.gameidx).name,self.player1,self.player2)]+self.movearray
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                            dfont = pygame.font.Font(None, 60)
                            text = dfont.render("d", False, (255, 255, 255))
                            self.screen.blit(text, (330, 580))
                            pygame.display.flip()
                        elif x in range(415, 600) and y in range(565, 630):
                            game=Game(self.gameidx).game
                            game = game(self.player1, self.player2, self.mode, self.screen,GameSelected, Resign, CommonWC, Pause,  self.movearray)
                            game.run()
                        elif x in range(630, 810) and y in range(565, 630):
                            gameselected = GameSelected(self.player1, self.player2,self.gameidx, self.screen)
                            gameselected.run()
        elif self.whowon==0:
            background = pygame.image.load("ItsaDraw.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 0), (415, 575, 215, 68), 4, 20)
            pygame.display.flip()
            running=True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running=False
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(220,390) and y in range(575,640):
                            game=Game(self.gameidx).game
                            game = game(self.player1, self.player2, self.mode, self.screen, GameSelected,Resign,CommonWC, Pause, self.movearray)
                            game.run()
                        elif x in range(420,625) and y in range(575,640):
                            self.movearray = [(datetime.now().replace(microsecond=0), Game(self.gameidx).name,self.player1, self.player2)] + self.movearray
                            with open("SavedGames.txt", "a") as SavedGames:
                                SavedGames.write(str(self.movearray) + "\n")
                            self.screen.blit(background, (0, 0))
                            pygame.display.flip()
                        elif x in range(650,800) and y in range(575,640):
                            gameselected = GameSelected(self.player1, self.player2,self.gameidx, self.screen)
                            gameselected.run()

class UpdateCSV:
    def __init__(self,player1,player2,game,result):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.result = result

    def run(self):
        Time = datetime.now().replace(microsecond=0 , second=0)
        with open("Serial.txt", "r", newline="") as Sno:
            Sno = int(Sno.read())
            Sno += 1
        with open("Serial.txt", "w") as NewSno:
            NewSno.write(str(Sno))
        with open("history.csv", "a",newline="") as history:
            append = csv.writer(history)
            append.writerow([Sno, Time,self.game, self.player1, self.player2, self.result])

class Pause:
    def __init__(self,player1,player2,board,screen,mode,movearray,gameidx,turn,t1,t2):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.screen = screen
        self.mode = mode
        self.movearray = movearray
        self.gameidx = gameidx
        self.turn=turn
        self.t1=t1
        self.t2=t2

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
                    print(pygame.mouse.get_pos())
                    x,y = pygame.mouse.get_pos()
                    if x in range(375,620) and y in range(470,540):
                        game=Game(self.gameidx).game
                        game=game(self.player1, self.player2, self.mode, self.screen,GameSelected, Resign, CommonWC, Pause,self.movearray, self.turn, self.t1, self.t2, time.time(), self.board)
                        game.run()
                    elif x in range(240,480) and y in range(560,630):
                        game = Game(self.gameidx).game
                        game = game(self.player1, self.player2, self.mode, self.screen, GameSelected, Resign, CommonWC, Pause, self.movearray)
                        game.run()
                    elif x in range(515,760) and y in range(565,630):
                        gameselected = GameSelected(self.player1, self.player2, self.gameidx, self.screen)
                        gameselected.run()

clock = pygame.time.Clock()
clock.tick(60)
pygame.init()
Bigscreen=pygame.display.set_mode((1000,700))
Biggame=FirstUI("Vijay Sir","Rajit",Bigscreen)
Biggame.run()
pygame.quit()