import pygame
import numpy as np
import time
import math
draw1=False
draw2=False

class TicTacToe:
    def __init__(self,player1,player2,mode,screen,GameSelected,Resign,CommonWC,Pause,movearray,t1=0,t2=0,turn=1,board=None,last_tick=time.time()):
        self.idx=0
        if int(mode) in {0,1,2}:
            self.player1=player1
            self.player2=player2
            self.screen=screen
            self.mode=mode
            self.GameSelected=GameSelected
            self.movearray=movearray
            self.Resign=Resign
            self.CommonWC=CommonWC
            self.board = board.copy() if board is not None else np.zeros((10,10))
            self.timed=(int(mode)!=mode)
            self.turn=turn
            self.Pause=Pause
            self.t1=t1
            self.t2=t2
            self.last_tick=last_tick
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
        if int(self.mode) in {0,2}:
            background = pygame.image.load("TicTacToeBackground.png")
            background = pygame.transform.scale(background, (1000, 700))
            font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 30)
            tfont = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 35)
            running = True
            global draw1, draw2
            draw1 = False
            draw2 = False
            while running:
                self.screen.blit(background, (0, 0))
                if self.timed:
                    presenttime = time.time()
                    dt = presenttime - self.last_tick
                    self.last_tick = presenttime

                    if self.turn == 1:
                        self.t1 -= dt
                        if self.t1 <= 0:
                            self.CommonWC(self.player1, self.player2, 2, self.mode+1, self.screen, self.movearray,
                                          self.idx).run()
                            return
                    else:
                        self.t2 -= dt
                        if self.t2 <= 0:
                            self.CommonWC(self.player1, self.player2, 1, self.mode+1, self.screen, self.movearray,
                                          self.idx).run()
                            return
                text = font.render(self.player1, False, (255, 255, 255))
                text.set_alpha(150)
                self.screen.blit(text, (145, 45))
                text = font.render(self.player2, False, (255, 255, 255))
                text.set_alpha(150)
                self.screen.blit(text, (640, 45))
                if draw1 and draw2:
                    draw1 = False
                    draw2 = False
                    self.turn = 1
                    self.movearray.append((0, "Match Drawn", 0))
                    self.CommonWC(self.player1, self.player2, 0, self.mode+self.timed, self.screen, self.movearray,self.idx).run()
                self.loadboard(self.board)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if (x-63)**2+(y-61)**2<2025:
                            self.Pause(self.player1,self.player2,self.board,self.screen,self.mode+self.timed,self.movearray,self.idx,self.turn,t1=self.t1,t2=self.t2).run()
                        if x in range(85, 215) and y in range(425, 475):
                            draw1 = not draw1
                        elif x in range(785, 915) and y in range(425, 475):
                            draw2 = not draw2
                        elif x in range(85, 215) and y in range(490, 545):
                            self.Resign(self.player1, self.player2, self.board, self.screen, self.mode+self.timed, 2,self.movearray,self.idx,self.turn,t1=self.t1,t2=self.t2,last_tick=self.last_tick).run()
                        elif x in range(780, 915) and y in range(490, 545):
                            self.Resign(self.player1, self.player2, self.board, self.screen, self.mode+self.timed, 1,self.movearray,self.idx,self.turn,t1=self.t1,t2=self.t2,last_tick=self.last_tick).run()
                        elif x in range(290, 710) and y in range(185, 580):
                            if (x - 290) % 43 < 33 and (y-185)%40 <32:
                                col = (x - 290) // 43
                                row = (y - 185) // 40
                                if self.board[col][row] ==0:
                                    self.board[col][row] = self.turn
                                    self.movearray.append((self.turn, col, int(row)))
                                    if self.turn == 1:
                                        img = pygame.image.load("lucky.png")
                                    else:
                                        img = pygame.image.load("MagicCatFace.png")
                                    img = pygame.transform.scale(img, (40, 40))
                                    self.screen.blit(img, (290 + 43 * col, 185 + 40 * row))
                                    pygame.display.flip()
                                    result = TicTacToeWC(self.board).run()
                                    if result != -1:
                                        self.turn = 1
                                        self.CommonWC(self.player1, self.player2, result, self.mode+self.timed, self.screen,self.movearray,self.idx).run()
                                    self.turn = 3 - self.turn
                if draw1:
                    pygame.draw.rect(self.screen, (255, 255, 255), (84, 426, 135, 58), 4, 20)
                if draw2:
                    pygame.draw.rect(self.screen, (255, 255, 255), (781, 425, 136, 54), 4, 20)
                if self.timed:
                    self.clock(150, 150, self.t1, self.turn == 1)
                    self.clock(850, 150, self.t2, self.turn == 2)
                    time1 = tfont.render(self.writetime(self.t1), True, (255, 255, 255))
                    time2 = tfont.render(self.writetime(self.t2), True, (255, 255, 255))

                    self.screen.blit(time1, (110, 330))
                    self.screen.blit(time2, (810, 330))


                pygame.display.flip()
        elif int(self.mode) == 1:
            if self.mode==1:
                background = pygame.image.load("TimeSelect.png")
                background = pygame.transform.scale(background, (1000, 700))
                self.screen.blit(background, (0, 0))
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            selected_time = None

                            if x in range(123, 227) and y in range(262, 390):
                                selected_time = 5
                                self.mode = 1.1
                            elif x in range(251, 387) and y in range(255, 391):
                                selected_time = 10
                                self.mode = 1.2
                            elif x in range(405, 569) and y in range(249, 413):
                                selected_time = 15
                                self.mode = 1.3
                            elif x in range(585, 729) and y in range(253, 413):
                                selected_time = 20
                                self.mode = 1.4
                            elif x in range(742, 910) and y in range(245, 405):
                                selected_time = 30
                                self.mode = 1.5
                            if selected_time is not None:
                                seconds = selected_time * 60
                                game = TicTacToe(self.player1, self.player2, self.mode - 1, self.screen,self.GameSelected, self.Resign, self.CommonWC, self.Pause,self.movearray,t1=seconds,t2=seconds, turn=1, last_tick=time.time())
                                game.run()
            else:
                game=TicTacToe(self.player1, self.player2, self.mode - 1, self.screen, self.GameSelected, self.Resign, self.CommonWC, self.Pause,self.movearray, t1=self.t1, t2=self.t2,turn=self.turn,board=self.board,last_tick=time.time())
                game.run()

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
    def __init__(self,board):
        self.board=board
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
