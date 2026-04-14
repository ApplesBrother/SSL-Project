import pygame
import numpy as np

draw1 = False
draw2 = False
turn = 1

class Connect4:
    def __init__(self,player1,player2,mode,screen, GameSelected, Resign, CommonWC, movearray):
        if mode==0:
            self.player1 = player1
            self.player2 = player2
            self.screen = screen
            self.mode=mode
            self.GameSelected = GameSelected
            self.movearray = movearray
            self.Resign = Resign
            self.CommonWC=CommonWC
            self.board=np.zeros((7,7))
        elif mode==1:
            self.player1 = player1
            self.player2 = player2
            self.screen = screen
            self.mode=mode
            self.board=np.zeros((7,7))
        elif mode==2:
            self.player1 = player1
            self.player2 = player2
            self.screen = screen
            self.mode=mode
        elif mode==3:
            self.player1 = player1
            self.player2 = player2
            self.screen = screen
            self.mode=mode
            self.board=np.zeros((7,7))
    def loadboard(self,board):
        for x,y in np.argwhere(board==1):
            background=pygame.image.load("lucky.png")
            background=pygame.transform.scale(background,(40,40))
            self.screen.blit(background,(295.5+61.4*x,190.5+57.5*y))
        for x,y in np.argwhere(board==2):
            background=pygame.image.load("MagicCatFace.png")
            background=pygame.transform.scale(background,(40,40))
            self.screen.blit(background,(295.5+61.4*x,190.5+57.5*y))
        pygame.display.flip()


    def run(self):
        if self.mode==0:
            background = pygame.image.load("Connect4Background.png")
            background = pygame.transform.scale(background, (1000, 700))
            self.screen.blit(background, (0, 0))
            font = pygame.font.Font("Fredoka_Expanded-Bold.ttf", 30)
            text = font.render(self.player1, False, (255, 255, 255))
            text.set_alpha(150)
            self.screen.blit(text, (145, 45))
            text = font.render(self.player2, False, (255, 255, 255))
            text.set_alpha(150)
            self.screen.blit(text, (640 , 45))
            self.loadboard(self.board)
            running = True
            global draw1, draw2, turn
            while running:
                if draw1 and draw2:
                    game = self.CommonWC(self.player1,self.player2,0,self.mode,self.screen,self.movearray)
                    game.run()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if x in range(85,215) and y in range(425,475):
                            draw1 = not draw1
                        elif x in range(785,915) and y in range(425,475):
                            draw2 = not draw2
                        elif x in range(85,215) and y in range(490,545):
                            resign=self.Resign(self.player1, self.player2,self.board,self.screen,self.mode,2, self.movearray)
                            resign.run()
                        elif x in range(780,915) and y in range(490,545):
                            resign=self.Resign(self.player1, self.player2,self.board, self.screen,self.mode,1,self.movearray)
                            resign.run()
                        elif x in range(290,710) and y in range(185,575):
                            if (x-290)%61<50:
                                n=(x-290)//61
                                if 0 not in self.board[n, :]:
                                    continue
                                arr= self.board[n,:]
                                y = np.where(arr== 0)[0]
                                y = y[-1]
                                self.board[n][y] = turn
                                if turn ==1:
                                    background = pygame.image.load("lucky.png")
                                    background = pygame.transform.scale(background, (40, 40))
                                    self.screen.blit(background, (295.5 + 61.4 * n, 190.5 + 57.5 * y))
                                elif turn ==2:
                                    background = pygame.image.load("MagicCatFace.png")
                                    background = pygame.transform.scale(background, (40, 40))
                                    self.screen.blit(background, (295.5 + 61.4 * n, 190.5 + 57.5 * y))
                                pygame.display.flip()
                                result=Connect4WC(self.player1,self.player2,self.board,self.mode).run()
                                if result!=-1:
                                    game=self.CommonWC(self.player1,self.player2,result,self.mode,self.screen,self.movearray)
                                    game.run()

                                turn=3-turn
            pygame.quit()

class Connect4WC:
    def __init__(self, player1, player2, board, mode):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.mode = mode

    def run(self):
        for i in (1, 2):
            if np.any(np.all(np.stack([self.board[:,j:j+4] for j in range(4)],axis=0)==i,axis=0)):
                return i
            if np.any(np.all(np.stack([self.board[j:j+4,:] for j in range(4)],axis=0)==i,axis=0)):
                return i
            if np.any(np.all(np.stack([self.board[j:j+4,j:j+4] for j in range(4)],axis=0)==i,axis=0)):
                return i
            if np.any(np.all(np.stack([self.board[j:j+4,3-j:7-j] for j in range(4)], axis=0)==i,axis=0)):
                return i
        if 0 not in self.board:
            return 0
        return -1


