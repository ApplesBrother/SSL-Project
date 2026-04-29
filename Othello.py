import pygame
import numpy as np
import time
import math

draw1 = False
draw2 = False

DIRECTIONS = np.array([
    [-1,-1], [-1,0], [-1,1],
    [0,-1],          [0,1],
    [1,-1],  [1,0],  [1,1]
])

class Othello:
    def __init__(self, player1, player2, mode, screen,
                 GameSelected, Resign, CommonWC, Pause,
                 movearray, t1=0, t2=0, turn=1,
                 board=None, last_tick=time.time()):

        self.idx = 2

        self.x0, self.y0 = 281, 181
        self.x1, self.y1 = 716, 587

        self.cell_w = (self.x1 - self.x0) / 8
        self.cell_h = (self.y1 - self.y0) / 8

        if int(mode) in {0,1,2}:
            self.player1 = player1
            self.player2 = player2
            self.screen = screen
            self.mode = mode
            self.GameSelected = GameSelected
            self.movearray = movearray
            self.Resign = Resign
            self.CommonWC = CommonWC
            self.Pause = Pause

            self.board = board.copy() if board is not None else np.zeros((8,8), dtype=int)

            if board is None:
                self.board[3,3] = 2
                self.board[3,4] = 1
                self.board[4,3] = 1
                self.board[4,4] = 2

            self.timed = (int(mode) != mode)
            self.turn = turn
            self.t1 = t1
            self.t2 = t2
            self.last_tick = last_tick

        elif mode == 3:
            self.player1 = player1
            self.player2 = player2
            self.screen = screen
            self.mode = mode
            self.movearray = movearray
            self.board = np.zeros((8,8), dtype=int)
            self.turn = 1

    def valid_moves(self, player):
        opponent = 3 - player
        valid_mask = np.zeros_like(self.board, dtype=bool)
        empty = np.argwhere(self.board == 0)

        for x, y in empty:
            for dx, dy in DIRECTIONS:
                cx, cy = x + dx, y + dy
                found = False

                while 0 <= cx < 8 and 0 <= cy < 8:
                    val = self.board[cx, cy]

                    if val == opponent:
                        found = True
                    elif val == player:
                        if found:
                            valid_mask[x, y] = True
                        break
                    else:
                        break

                    cx += dx
                    cy += dy

        return np.argwhere(valid_mask)

    def apply_move(self, x, y, player):
        opponent = 3 - player
        flip_mask = np.zeros_like(self.board, dtype=bool)

        for dx, dy in DIRECTIONS:
            cx, cy = x + dx, y + dy
            temp_mask = np.zeros_like(self.board, dtype=bool)

            while 0 <= cx < 8 and 0 <= cy < 8:
                val = self.board[cx, cy]

                if val == opponent:
                    temp_mask[cx, cy] = True
                elif val == player:
                    if np.any(temp_mask):
                        flip_mask |= temp_mask
                    break
                else:
                    break

                cx += dx
                cy += dy

        self.board[flip_mask] = player
        self.board[x, y] = player

    def loadboard(self, board):
        for x, y in np.argwhere(board == 1):
            img = pygame.image.load("lucky.png")
            img = pygame.transform.scale(img, (40,40))
            self.screen.blit(img, (281 + 56*x, 182 + 51.5*y))

        for x, y in np.argwhere(board == 2):
            img = pygame.image.load("MagicCatFace.png")
            img = pygame.transform.scale(img, (40,40))
            self.screen.blit(img, (280 + 56*x, 183 + 51.5*y))

    def draw_valid_moves(self, moves):
        color = (0,0,0) if self.turn == 1 else (255,255,255)

        for x, y in moves:
            cx = int(self.x0 + self.cell_w * x + self.cell_w / 2)
            cy = int(self.y0 + self.cell_h * y + self.cell_h / 2)
            pygame.draw.circle(self.screen, color, (cx, cy), 6)

    def clock(self, x, y, tleft, on):
        color = (200,200,200) if on else (120,120,120)
        pygame.draw.circle(self.screen, color, (x,y), 70, 3)

        angle = (int(tleft)%60)*6
        rad = math.radians(angle-90)

        hx = x + 55*math.cos(rad)
        hy = y + 55*math.sin(rad)

        pygame.draw.line(self.screen, color, (x,y), (hx,hy), 3)

    def writetime(self, t):
        t = max(0,int(t))
        return f"{t//60}:{t%60:02d}"

    def run(self):
        global draw1, draw2

        if int(self.mode) in {0,2}:

            background = pygame.image.load("OthelloBackground.png")
            background = pygame.transform.scale(background,(1000,700))

            font = pygame.font.Font("Fredoka_Expanded-Bold.ttf",30)
            tfont = pygame.font.Font("Fredoka_Expanded-Bold.ttf",35)

            running = True
            draw1 = False
            draw2 = False

            while running:
                self.screen.blit(background,(0,0))

                if draw1 and draw2:
                    draw1 = False
                    draw2 = False
                    self.turn = 1
                    self.movearray.append((0, "Match Drawn", 0))
                    self.CommonWC(self.player1,self.player2,0,
                        self.mode+self.timed,self.screen,
                        self.movearray,self.idx).run()
                    return

                if self.timed:
                    now = time.time()
                    dt = now - self.last_tick
                    self.last_tick = now

                    if self.turn == 1:
                        self.t1 -= dt
                        if self.t1 <= 0:
                            self.CommonWC(self.player1,self.player2,2,
                                self.mode+1,self.screen,self.movearray,self.idx).run()
                            return
                    else:
                        self.t2 -= dt
                        if self.t2 <= 0:
                            self.CommonWC(self.player1,self.player2,1,
                                self.mode+1,self.screen,self.movearray,self.idx).run()
                            return

                self.screen.blit(font.render(self.player1,False,(255,255,255)),(145,45))
                self.screen.blit(font.render(self.player2,False,(255,255,255)),(640,45))

                self.loadboard(self.board)

                moves = self.valid_moves(self.turn)
                self.draw_valid_moves(moves)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = pygame.mouse.get_pos()

                        if (x-63)**2 + (y-61)**2 < 2025:
                            self.Pause(self.player1,self.player2,self.board,
                                self.screen,self.mode+self.timed,
                                self.movearray,self.idx,self.turn,
                                t1=self.t1,t2=self.t2).run()

                        if 85 <= x <= 215 and 425 <= y <= 475:
                            draw1 = not draw1

                        elif 785 <= x <= 915 and 425 <= y <= 475:
                            draw2 = not draw2

                        elif 85 <= x <= 215 and 490 <= y <= 545:
                            self.Resign(self.player1,self.player2,self.board,
                                self.screen,self.mode+self.timed,2,
                                self.movearray,self.idx,self.turn,
                                t1=self.t1,t2=self.t2,
                                last_tick=self.last_tick).run()
                            return

                        elif 780 <= x <= 915 and 490 <= y <= 545:
                            self.Resign(self.player1,self.player2,self.board,
                                self.screen,self.mode+self.timed,1,
                                self.movearray,self.idx,self.turn,
                                t1=self.t1,t2=self.t2,
                                last_tick=self.last_tick).run()
                            return

                        if self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1:
                            gx = int((x - self.x0) / self.cell_w)
                            gy = int((y - self.y0) / self.cell_h)

                            if any((gx==m[0] and gy==m[1]) for m in moves):
                                self.apply_move(gx,gy,self.turn)
                                self.movearray.append((self.turn,gx,gy))

                                self.turn = 3 - self.turn

                                if len(self.valid_moves(self.turn)) == 0:
                                    self.turn = 3 - self.turn

                                if len(self.valid_moves(1)) == 0 and len(self.valid_moves(2)) == 0:
                                    result = OthelloWC(self.board).run()
                                    self.CommonWC(self.player1,self.player2,result,
                                        self.mode+self.timed,self.screen,
                                        self.movearray,self.idx).run()
                                    return

                if draw1:
                    pygame.draw.rect(self.screen, (255,255,255), (84,424,135,55), 4, 20)
                if draw2:
                    pygame.draw.rect(self.screen, (255,255,255), (781,425,136,54), 4, 20)

                if self.timed:
                    self.clock(150,150,self.t1,self.turn==1)
                    self.clock(850,150,self.t2,self.turn==2)

                    self.screen.blit(tfont.render(self.writetime(self.t1),True,(255,255,255)),(110,230))
                    self.screen.blit(tfont.render(self.writetime(self.t2),True,(255,255,255)),(810,230))

                pygame.display.flip()

        elif int(self.mode) == 1:
            background = pygame.image.load("TimeSelect.png")
            background = pygame.transform.scale(background,(1000,700))

            self.screen.blit(background,(0,0))
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = pygame.mouse.get_pos()

                        options = {
                            (123,227,262,390):5,
                            (251,387,255,391):10,
                            (405,569,249,413):15,
                            (585,729,253,413):20,
                            (742,910,245,405):30
                        }

                        for (x1,x2,y1,y2), mins in options.items():
                            if x1<=x<=x2 and y1<=y<=y2:
                                sec = mins*60
                                Othello(self.player1,self.player2,
                                    self.mode-1,self.screen,
                                    self.GameSelected,self.Resign,
                                    self.CommonWC,self.Pause,
                                    self.movearray,
                                    t1=sec,t2=sec).run()

        elif self.mode == 3:
            background = pygame.image.load("SavedGames.png")
            background = pygame.transform.scale(background,(1000,700))

            self.screen.blit(background,(0,0))
            pygame.display.flip()

class OthelloWC:
    def __init__(self, board):
        self.board = board

    def run(self):
        if np.any(self.board == 0):
            return -1

        counts = np.bincount(self.board.ravel(), minlength=3)

        if counts[1] > counts[2]: return 1
        if counts[2] > counts[1]: return 2
        return 0
