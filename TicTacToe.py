import pygame
import numpy as np
import time
import math


draw1=False
draw2=False

class TicTacToe:
    def __init__(self,player1,player2,mode,screen,GameSelected,Resign,CommonWC,Pause,movearray,turn=1,t1=10,t2=10,last_tick=None,board=None):
        self.idx=0
        if mode in {0,1,2}:
            self.player1=player1
            self.player2=player2
            self.screen=screen
            self.mode=mode
            self.GameSelected=GameSelected
            self.movearray=movearray
            self.Resign=Resign
            self.CommonWC=CommonWC
            self.board = board.copy() if board is not None else np.zeros((10,10))
            self.timed=(mode==1)
            self.t1=t1
            self.t2=t2
            self.last_tick = last_tick if last_tick is not None else time.time()
            self.turn=turn
            self.Pause=Pause
        elif mode==3:
            self.player1 = player1
            self.player2 = player2
            self.screen = screen
            self.mode = mode
            self.movearray = movearray
            self.board = np.zeros((10, 10))
            self.turn = 1

    def loadboard(self,board):
        for x,y in np.argwhere(board==1):
            img=pygame.image.load("lucky.png")
            img=pygame.transform.scale(img,(40,40))
            self.screen.blit(img,(287+42.8*x,183+40.3*y))
        for x,y in np.argwhere(board==2):
            img=pygame.image.load("MagicCatFace.png")
            img=pygame.transform.scale(img,(40,40))
            self.screen.blit(img,(287+42.8*x,183+40.3*y))

    def clock(self,x,y,tleft,on):
        color=(200,200,200) if on else (120,120,120)
        pygame.draw.circle(self.screen,color,(x,y),70,3)
        seconds=int(tleft)
        angle=(seconds%60)*6
        rad=math.radians(angle-90)
        hx=x+55*math.cos(rad)
        hy=y+55*math.sin(rad)
        pygame.draw.line(self.screen,color,(x,y),(hx,hy),3)

    def writetime(self,t):
        t=max(0,int(t))
        return f"{t//60}:{t%60:02d}"

    def run(self):
        if self.mode in {0,1,2}:
            background = pygame.image.load("TicTacToeBackground.png")
            background = pygame.transform.scale(background, (1002, 700))
            font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 30)
            tfont = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 35)
            running = True
            global draw1, draw2
            draw1 = False
            draw2 = False
            while running:
                self.screen.blit(background, (0, 0))
                text = font.render(self.player1, False, (255, 255, 255))
                text.set_alpha(150)
                self.screen.blit(text, (145, 45))
                text = font.render(self.player2, False, (255, 255, 255))
                text.set_alpha(150)
                self.screen.blit(text, (640, 45))
                if self.timed:
                    presenttime = time.time()
                    dt = presenttime - self.last_tick
                    self.last_tick = presenttime
                    if self.turn == 1:
                        self.t1 -= dt
                    else:
                        self.t2-=dt
                    t1 = tfont.render(self.writetime(self.t1), False, (255, 255, 255))
                    t2 = tfont.render(self.writetime(self.t2), False, (255, 255, 255))
                    self.screen.blit(t1, (120, 185))
                    self.screen.blit(t2, (810, 185))
                    self.clock(160, 300, self.t1, self.turn == 1)
                    self.clock(845, 300, self.t2, self.turn == 2)
                    if self.t1<0:
                        self.turn = 1
                        self.CommonWC(self.player1, self.player2, 2, self.mode, self.screen, self.movearray,self.idx).run()
                    if self.t2<0:
                        self.turn = 1
                        self.CommonWC(self.player1, self.player2, 1, self.mode, self.screen, self.movearray,self.idx).run()
                if draw1 and draw2:
                    draw1 = False
                    draw2 = False
                    self.turn = 1
                    self.movearray.append((0, "Match Drawn", 0))
                    self.CommonWC(self.player1, self.player2, 0, self.mode, self.screen, self.movearray,self.idx).run()
                self.loadboard(self.board)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if (x-63)**2+(y-61)**2<2025:
                            self.Pause(self.player1,self.player2,self.board,self.screen,self.mode,self.movearray,self.idx,self.turn,self.t1,self.t2).run()
                        if x in range(85, 215) and y in range(425, 475):
                            draw1 = not draw1
                        elif x in range(785, 915) and y in range(425, 475):
                            draw2 = not draw2
                        elif x in range(85, 215) and y in range(490, 545):
                            self.Resign(self.player1, self.player2, self.board, self.screen, self.mode, 2,self.movearray,self.idx,self.turn,self.t1,self.t2,self.last_tick).run()
                        elif x in range(780, 915) and y in range(490, 545):
                            self.Resign(self.player1, self.player2, self.board, self.screen, self.mode, 1,self.movearray,self.idx,self.turn,self.t1,self.t2,self.last_tick).run()
                        elif x in range(290, 710) and y in range(185, 580):
                            if (x - 290) % 43 < 33 and (y - 185) % 40 < 32:
                                col = (x - 290) // 43
                                row = (y - 185) // 40
                                if(self.board[col][row] == 0):
                                    print(col,row)
                                    self.board[col][row] = self.turn
                                    self.movearray.append((self.turn, col, int(row)))
                                    if self.turn == 1:
                                        img = pygame.image.load("lucky.png")
                                    else:
                                        img = pygame.image.load("MagicCatFace.png")
                                    img = pygame.transform.scale(img, (40, 40))
                                    self.screen.blit(img, (290 + 43 * col, 185 + 40 * row))
                                    pygame.display.flip()
                                    result = TicTacToeWC(self.player1, self.player2, self.board, self.mode).run()
                                    if result != -1:
                                        self.turn = 1
                                        game = self.CommonWC(self.player1, self.player2, result, self.mode, self.screen,
                                                             self.movearray, self.idx)
                                        game.run()
                                        return
                                    self.turn = 3 - self.turn
                                    if self.timed:
                                        self.last_tick = time.time()
                if draw1:
                    pygame.draw.rect(self.screen, (255, 255, 255), (84, 426, 135, 58), 4, 20)
                if draw2:
                    pygame.draw.rect(self.screen, (255, 255, 255), (781, 425, 136, 54), 4, 20)
                pygame.display.flip()
        elif self.mode==3:
            background = pygame.image.load("SavedGames.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            pygame.display.flip()
            clock = pygame.time.Clock()
            running = True
            sortedarray=[]
            for i in range(len(self.movearray)):
                if self.movearray[i][0].type!=str:
                    sortedarray.append(self.movearray[i][1])
            while running:
                self.screen.blit(background, (0, 0))
                self.loadboard(self.board)
                pygame.display.flip()
                clock.tick(30)

class TicTacToeWC:
    def __init__(self,player1,player2,board,mode):
        self.player1=player1
        self.player2=player2
        self.board=board
        self.mode=mode
    def run(self):
        for i in (1,2):
            if np.any(np.all(np.stack([self.board[:,j:j+5] for j in range(5)],axis=0)==i,axis=0)):
                return i
            if np.any(np.all(np.stack([self.board[j:j+5,:] for j in range(5)],axis=0)==i,axis=0)):
                return i
            if np.any(np.all(np.stack([self.board[j:j+5,j:j+5] for j in range(5)],axis=0)==i,axis=0)):
                return i
            if np.any(np.all(np.stack([self.board[j:j+5,5-j:10-j] for j in range(5)],axis=0)==i,axis=0)):
                return i
        if 0 not in self.board:
            return 0
        return -1