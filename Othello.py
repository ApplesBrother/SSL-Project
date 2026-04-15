import pygame
import numpy as np
import time
import math
draw1=False
draw2=False
turn=1

class Othello:
    def __init__(self,player1,player2,mode,screen,GameSelected,Resign,CommonWC,UpdateCSV,movearray):
        if mode in {0,1}:
            self.player1=player1
            self.player2=player2
            self.screen=screen
            self.mode=mode
            self.GameSelected=GameSelected
            self.movearray=movearray
            self.Resign=Resign
            self.CommonWC=CommonWC

            self.board=np.zeros((8,8))
            self.board[3][3]=self.board[4][4]=2
            self.board[3][4]=self.board[4][3]=1
            
            self.timed=(mode==1)
            self.t1=10
            self.t2=10
            self.last_tick=time.time()
            self.turn=1
            self.UpdateCSV=UpdateCSV

        elif mode==2:
            self.player1=player1
            self.player2=player2
            self.screen=screen
            self.mode=mode
        elif mode==3:
            self.player1=player1
            self.player2=player2
            self.screen=screen
            self.mode=mode

    def loadboard(self,board):
        for row,col in np.argwhere(board==1):
            background=pygame.image.load("lucky.png")
            background=pygame.transform.scale(background,(33,33))
            self.screen.blit(background,(287+56*col,187+51.5*row))
        for row,col in np.argwhere(board==2):
            background=pygame.image.load("MagicCatFace.png")
            background=pygame.transform.scale(background,(33,33))
            self.screen.blit(background,(287+56*col,187+51.5*row))
        pygame.display.flip()

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
    
    def valid_move(self,r,c,player):
        if self.board[r][c]!=0:
            return False
        
        opponent=3-player
        directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        for dr,dc in directions:
            x, y = r + dr, c + dc
            
            if not (0<=x<8 and 0<=y<8):
                continue
            if self.board[x][y]!=opponent:
                continue

            while 0<=x<8 and 0<=y<8:
                if self.board[x][y]==opponent:
                    x+=dr
                    y+=dc
                elif self.board[x][y]==player:
                    return True
                else:
                    break
            
        return False
    
    def flip_pieces(self,r,c,player):
        opponent=3-player
        directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        for dr,dc in directions:
            x, y = r + dr, c + dc
            to_flip=[]

            if not (0<=x<8 and 0<=y<8):
                continue
            if self.board[x][y]!=opponent:
                continue

            while 0<=x<8 and 0<=y<8:
                if self.board[x][y]==opponent:
                    to_flip.append((x,y))
                elif self.board[x][y]==player:
                    for fx,fy in to_flip:
                        self.board[fx][fy]=player
                    break
                else:
                    break
                x+=dr
                y+=dc

    def run(self):
        if self.mode in {0,1}:
            background = pygame.image.load("OthelloBackground.png")
            background = pygame.transform.scale(background, (1000, 700))
            font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 30)
            tfont = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 35)
            running = True
            global draw1, draw2
            draw1 = False
            draw2 = False
            self.movearray.append((0,"Connect4",0))
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
                        game = self.CommonWC(self.player1, self.player2, 2, self.mode, self.screen, self.movearray)
                        game.run()
                        return
                    if self.t2<0:
                        self.turn = 1
                        game = self.CommonWC(self.player1, self.player2, 1, self.mode, self.screen, self.movearray)
                        game.run()
                        return
                if draw1 and draw2:
                    draw1 = False
                    draw2 = False
                    self.turn = 1
                    self.movearray.append((0, "Match Drawn", 0))
                    game=self.UpdateCSV(self.player1,self.player2,"Connect4",0)
                    game.run()
                    game = self.CommonWC(self.player1, self.player2, 0, self.mode, self.screen, self.movearray)
                    game.run()
                    return
                self.loadboard(self.board)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(85, 215) and y in range(425, 475):
                            draw1 = not draw1
                        elif x in range(785, 915) and y in range(425, 475):
                            draw2 = not draw2
                        elif x in range(85, 215) and y in range(490, 545):
                            self.turn = 1
                            resign = self.Resign(self.player1, self.player2, self.board, self.screen, self.mode, 2,
                                                 self.movearray)
                            resign.run()
                            return
                        elif x in range(780, 915) and y in range(490, 545):
                            self.turn = 1
                            resign = self.Resign(self.player1, self.player2, self.board, self.screen, self.mode, 1,
                                                 self.movearray)
                            resign.run()
                            return
                        elif x in range(290, 710) and y in range(185, 575):
                            if (x - 290) % 53 < 42:
                                col = (x - 290) // 53
                            if (y - 185) % 53 < 42:
                                row = (y - 185) // 53

                                if self.board[row][col] != 0:
                                    continue

                                if not self.valid_move(row,col,self.turn):
                                    continue
                                
                                self.board[row][col] = self.turn
                                self.flip_pieces(row,col,self.turn)

                                self.movearray.append((self.turn,col,int(row)))
                                if self.turn == 1:
                                    img = pygame.image.load("lucky.png")
                                else:
                                    img = pygame.image.load("MagicCatFace.png")
                                img = pygame.transform.scale(img, (33, 33))
                                self.screen.blit(img, (287 + 56 * col, 187 + 51.5 * row))
                                pygame.display.flip()
                                result = OthelloWC(self.player1, self.player2, self.board, self.mode).run()
                                if result != -1:
                                    self.turn = 1
                                    game=self.UpdateCSV(self.player1, self.player2, "Othello",result)
                                    game.run()
                                    game=self.CommonWC(self.player1, self.player2, result, self.mode, self.screen,
                                                         self.movearray)
                                    game.run()
                                    return
                                self.turn = 3 - self.turn
                                if not any(self.valid_move(r,c,self.turn) for r in range(8) for c in range(8) if self.board[r][c]==0):
                                    self.turn = 3 - self.turn
                                if self.timed:
                                    self.last_tick = time.time()
                pygame.display.flip()
            pygame.quit()

class OthelloWC:
    def __init__(self,player1,player2,board,mode):
        self.player1=player1
        self.player2=player2
        self.board=board
        self.mode=mode
    def run(self):
        if np.any(self.board==0):
            return -1
        
        p1 = np.sum(self.board==1)
        p2 = np.sum(self.board==2)

        if p1>p2:
            return 1
        elif p2>p1:
            return 2
        else:
            return 0

class Timer:
    def __init__(self,player1,player2,screen):
        self.player1=player1
        self.player2=player2
        self.screen=screen
