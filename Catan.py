import pygame
import numpy as np
import time
import math
import random

class Catan:
    def __init__(self,player1,player2,mode,screen,GameSelected,Resign,CommonWC,UpdateCSV,movearray):
        self.player1=player1
        self.player2=player2
        self.screen=screen
        self.mode=mode
        self.GameSelected=GameSelected
        self.movearray=movearray
        self.Resign=Resign
        self.CommonWC=CommonWC
        self.movearray.append((0, "Catan", 0))
        self.UpdateCSV = UpdateCSV

        self.font_big = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.x1, self.y1 = 290, 185
        self.x2, self.y2 = 710, 575
        self.size = 80

        self.tiles = {
            "wood": pygame.image.load("wood.png"),
            "brick": pygame.image.load("brick.png"),
            "wool": pygame.image.load("wool.png"),
            "wheat": pygame.image.load("wheat.png"),
            "ore": pygame.image.load("ore.png"),
            "desert": pygame.image.load("desert.png")
        }

        hex_width = int(self.size * 2)
        hex_height = int(math.sqrt(3) * self.size)
        for k in self.tiles:
            self.tiles[k] = pygame.transform.scale(self.tiles[k], (hex_width, hex_height))
        
        self.generate_tiles()
        self.build_graph()

        self.settlement_imgs = {
            1: pygame.transform.scale(pygame.image.load("settlement_p1.png"), (30, 30)),
            2: pygame.transform.scale(pygame.image.load("settlement_p2.png"), (30, 30))
        }

        self.road_imgs = {
            1: pygame.transform.scale(pygame.image.load("road_p1.png"), (40, 10)),
            2: pygame.transform.scale(pygame.image.load("road_p2.png"), (40, 10))
        }

        self.robber_img = pygame.transform.scale(pygame.image.load("robber.png"), (40, 40))

        self.structures = {
            1: {"settlement": 4, "city": 3, "road": 10},
            2: {"settlement": 4, "city": 3, "road": 10}
        }

        self.vertex_owner = {}
        self.vertex_type = {}
        self.edge_owner = {}

        self.turn = random.choice([1, 2])

        self.phase = "setup"
        self.setup_moves = {1: 0, 2: 0}

        self.setup_stage = "settlement"

        self.resources = {
            1: {"wood": 0, "brick": 0, "wool": 0, "wheat": 0, "ore": 0},
            2: {"wood": 0, "brick": 0, "wool": 0, "wheat": 0, "ore": 0}
        }

        self.last_roll = None

        self.has_rolled = False
        self.turn_phase = "roll"
        self.build_mode = False
        self.build_type = None

        self.robber_pos = None
        self.moving_robber = False

        self.knights_used = {1: 0, 2: 0}
        self.free_road = False

        self.message = ""
        self.message_timer = 0
        self.message_start_time = 0

        self.longest_road_owner = None
        self.longest_road_length = 0

        self.largest_army_owner = None
        self.largest_army_size = 0

        self.maritime_mode = False
        self.port_mode = False

        self.trade_give = None
        self.trade_get_mode = False

        self.player_trade_mode = False
        self.trade_offer = None
        self.awaiting_response = False

    def show_message(self, text, duration = 2):
        self.message = text
        self.message_timer = duration
        self.message_start_time = time.time()
    
    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def axial_to_pixel(self,q,r):
        x = self.center_x + self.size * (1.5 * q)
        y = self.center_y + self.size * (q/2 + r) * math.sqrt(3)
        return int(x), int(y)
    
    def generate_tiles(self):
        self.positions = [(0,0), (1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)]
        self.center_x, self.center_y = 500, 380

        resources = ["wood", "wood", "brick", "brick", "wool", "wheat", "ore"]
        random.shuffle(resources)

        numbers = [2, 3, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 11, 12]
        random.shuffle(numbers)

        self.board = {}
        self.title_numbers = {}

        center_resource = random.choice(["wood", "brick"])
        resources = ["wood", "wood", "brick", "brick", "wool", "wheat", "ore"]
        resources.remove(center_resource)
        random.shuffle(resources)

        for pos in self.positions:
            if pos == (0, 0):
                self.board[pos] = center_resource
            else:
                self.board[pos] = resources.pop()
            self.title_numbers[pos] = [numbers.pop(), numbers.pop()]
        
        self.ring = [(1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)]
        self.ports = {}

        ring_resources = [self.board[pos] for pos in self.ring]
        dup_resources = [r for r in set(ring_resources) if ring_resources.count(r) == 2]

        dup_resources = dup_resources[0]

        dup_positions = [pos for pos in self.ring if self.board[pos] == dup_resources]
        chosen_tile = random.choice(dup_positions)

        for i, pos in enumerate(self.ring):
            next_pos = self.ring[(i + 1) % 6]
            resource = self.board[pos]

            if pos == chosen_tile:
                self.ports[next_pos] = "3:1"
            else:
                if next_pos not in self.ports:
                    self.ports[next_pos] = f"{resource} 2:1"



    def get_hex_vertices(self, q, r):
        cx, cy = self.axial_to_pixel(q, r)

        vertices = []
        for i in range(6):
            angle = math.radians(60 * i)
            x = cx + self.size * math.cos(angle)
            y = cy + self.size * math.sin(angle)
            vertices.append((round(x,2), round(y,2)))
                
        return vertices
    
    def build_graph(self):
        self.vertices = {}
        self.edges = {}
        self.vertex_neighbors = {}
        self.edge_map = {}

        vertex_id = 0
        edge_id = 0

        vertex_lookup = {}

        for pos in self.positions:
            hex_vertices = self.get_hex_vertices(pos[0], pos[1])

            ids = []
            for v in hex_vertices:
                key = (round(v[0]/10), round(v[1]/10))
                if key not in vertex_lookup:
                    vertex_lookup[key] = vertex_id
                    self.vertices[vertex_id] = v
                    self.vertex_neighbors[vertex_id] = set()
                    vertex_id += 1
                
                ids.append(vertex_lookup[key])

            for i in range(6):
                v1 = ids[i]
                v2 = ids[(i + 1) % 6]

                edge_key = tuple(sorted((v1, v2)))

                if edge_key not in self.edge_map:
                    self.edge_map[edge_key] = edge_id
                    self.edges[edge_id] = edge_key
                    self.vertex_neighbors[v1].add(v2)
                    self.vertex_neighbors[v2].add(v1)
                    edge_id += 1
            
    def total_cards(self, player):
        return sum(self.resources[player].values())
    
    def get_clicked_tile(self, pos):
        mx, my = pos

        for (q,r) in self.positions:
            x, y = self.axial_to_pixel(q, r)
            if (mx - x) ** 2 + (my - y) ** 2 <= (self.size * 0.8) ** 2:
                return (q, r)
        
        return None

    def get_clicked_vertex(self, pos):
        mx, my = pos

        for v, (x, y) in self.vertices.items():
            if (mx - x) ** 2 + (my - y) ** 2 <= 15 ** 2:
                return v
        return None
    
    def get_clicked_edge(self, pos):
        mx, my = pos

        for e, (v1, v2) in self.edges.items():
            x1, y1 = self.vertices[v1]
            x2, y2 = self.vertices[v2]

            dx = x2 - x1
            dy = y2 - y1
            if dx == dy == 0:
                continue

            t = max(0, min(1, ((mx - x1) * dx + (my - y1) * dy) / (dx * dx + dy * dy)))
            px = x1 + t * dx
            py = y1 + t * dy

            dist = (mx - px) ** 2 + (my - py) ** 2
            if dist <= 15 ** 2:
                return e
            
        return None
    
    def can_place_settlement(self, v):
        if v in self.vertex_owner:
            return False

        x1, y1 = self.vertices[v]
        for other in self.vertex_owner:
            x2, y2 = self.vertices[other]
            dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
            if dist <= (self.size * 1.1) ** 2:
                return False
        
        if self.phase == "setup":
            return True
        
        for e, (v1, v2) in self.edges.items():
            if v in (v1, v2) and self.edge_owner.get(e) == self.turn:
                return True
            
        return False
    
    def can_place_road(self, e):
        if e in self.edge_owner:
            return False
            
        v1, v2 = self.edges[e]

        if self.phase == "setup":
            v1, v2 = self.edges[e]
            return self.last_settlement in (v1, v2)
            
        if (v1 in self.vertex_owner and self.vertex_owner[v1] == self.turn) or (v2 in self.vertex_owner and self.vertex_owner[v2] == self.turn):
            return True
        
        for other_e, owner in self.edge_owner.items():
            if owner == self.turn:
                ov1, ov2 = self.edges[other_e]
                if v1 in (ov1, ov2) or v2 in (ov1, ov2):
                    return True
            
        return False
    
    def distribute_resources(self, roll):
        if roll == 7:
            return

        for pos, nums in self.title_numbers.items():
            if roll in nums:
                if self.robber_pos == pos:
                    continue
                resource = self.board[pos]
                if resource == "desert":
                    continue

                hex_vertices = self.get_hex_vertices(pos[0], pos[1])

                for v_id, (vx, vy) in self.vertices.items():
                    for hx, hy in hex_vertices:
                        if abs(vx - hx) < 5 and abs(vy - hy) < 5:
                            if v_id in self.vertex_owner:
                                player = self.vertex_owner[v_id]
                                if self.vertex_type[v_id] == "settlement":
                                    self.resources[player][resource] += 1
                                elif self.vertex_type[v_id] == "city":
                                    self.resources[player][resource] += 2
    
    def can_afford(self, player, build_type):
        cost = {
            "Road": {"wood": 1, "brick": 1},
            "Settlement": {"wood": 1, "brick": 1, "wool": 1, "wheat": 1},
            "City": {"wheat": 2, "ore": 3},
            "Dev Card": {"wheat": 1, "wool": 1, "ore": 1}
        }

        for res, amt in cost[build_type].items():
            if self.resources[player][res] < amt:
                return False
        return True
    
    def pay_cost(self, player, build_type):
        cost = {
            "Road": {"wood": 1, "brick": 1},
            "Settlement": {"wood": 1, "brick": 1, "wool": 1, "wheat": 1},
            "City": {"wheat": 2, "ore": 3},
            "Dev Card": {"wheat": 1, "wool": 1, "ore": 1}
        }

        for res, amt in cost[build_type].items():
            self.resources[player][res] -= amt

    def discard_half(self, player):
        total = self.total_cards(player)
        if total < 7:
            return
        
        to_discard = total // 2

        for _ in range(to_discard):
            available = [res for res in self.resources[player] if self.resources[player][res] > 0]
            if not available:
                break

            chosen = random.choice(available)
            self.resources[player][chosen] -= 1

    def steal_from_opponent(self, tile):
        opponent = 3 - self.turn

        hex_vertices = self.get_hex_vertices(tile[0], tile[1])

        victim_has_building = False

        for v_id, (vx, vy) in self.vertices.items():
            for hx, hy in hex_vertices:
                if abs(vx - hx) < 5 and abs(vy - hy) < 5:
                    if v_id in self.vertex_owner and self.vertex_owner[v_id] == opponent:
                        victim_has_building = True
                        break
        
        if not victim_has_building:
            return
        
        available = [res for res in self.resources[opponent] if self.resources[opponent][res] > 0]
        if not available:
            return
        
        stolen = random.choice(available)

        self.resources[opponent][stolen] -= 1
        self.resources[self.turn][stolen] += 1

    def play_dev_card(self):
        roll = random.random()

        if roll < 0.7:
            self.knights_used[self.turn] += 1
            self.moving_robber = True
            self.show_message("Knight Card! Move the robber")

            count = self.knights_used[self.turn]

            if count >= 3 and count > self.largest_army_size:
                self.largest_army_size = count
                self.largest_army_owner = self.turn
                self.show_message(f"Player {self.turn} gets Largest Army!")
                if self.check_win():
                    return

        elif roll < 0.8:
            self.play_monopoly
            self.show_message("Monopoly Card!")

        elif roll < 0.9:
            self.free_road
            self.show_message("Free Road Card!")

        else:
            self.play_year_of_plenty
            self.show_message("Year of Plenty: +2 Resources!")
        
        if self.check_win():
            return
    
    def play_monopoly(self):
        resource = random.choice(["wood", "brick", "wool", "wheat", "ore"])
        opponent = 3 - self.turn

        amount = self.resources[opponent][resource]
        self.resources[opponent][resource] = 0
        self.resources[self.turn][resource] += amount

    def play_year_of_plenty(self):
        for _ in range(2):
            resource = random.choice(["wood", "brick", "wool", "wheat", "ore"])
            self.resources[self.turn][resource] += 1
        
    def get_longest_road(self, player):

        player_edges = [self.edges[e] for e in self.edge_owner if self.edge_owner[e] == player]

        graph = {}

        for v1, v2 in player_edges:
            if v1 not in graph:
                graph[v1] = []
            if v2 not in graph:
                graph[v2] = []

            graph[v1].append(v2)
            graph[v2].append(v1)

        def dfs(v, visited_edges):
            max_len = 0
            for nei in graph.get(v, []):
                if (v, nei) in visited_edges or (nei, v) in visited_edges:
                    continue

                visited_edges.add((v, nei))
                length = 1 + dfs(nei, visited_edges)
                visited_edges.remove((v, nei))

                max_len = max(max_len, length)

            return max_len

        best = 0
        for v in graph:
            best = max(best, dfs(v, set()))

        return best

        
    def get_victory_points(self, player):
        points = 0

        for v, owner in self.vertex_owner.items():
            if owner == player:
                if self.vertex_type.get(v) == "city":
                    points += 2
                else:
                    points +=1
                
        if self.longest_road_owner == player:
            points += 1
        
        if self.largest_army_owner == player:
            points +=1
        
        return points
    
    def maritime_trade(self, give_res, get_res):
        if self.resources[self.turn][give_res] >= 4:
            self.resources[self.turn][give_res] -= 4
            self.resources[self.turn][get_res] += 1
    
    def has_port(self, player, port_type):
        for pos, port in self.ports.items():
            hex_vertices = self.get_hex_vertices(pos[0], pos[1])

            for v_id, (vx, vy) in self.vertices.items():
                for hx, hy in hex_vertices:
                    if abs(vx - hx) < 5 and abs(vy - hy) < 5:
                        if v_id in self.vertex_owner and self.vertex_owner[v_id] == player:
                            if port_type == "3:1" and port == "3:1":
                                return True
                            if port_type in port:
                                return True
        return False
        
    def port_trade(self, give_res, get_res):

        has_2to1 = self.has_port(self.turn, give_res)
        has_3to1 = self.has_port(self.turn, "3:1")

        if has_2to1:
            cost = 2
        elif has_3to1:
            cost = 3
        else:
            self.show_message("No port access")
            return 

        if self.resources[self.turn][give_res] < cost:
            self.show_message("Not enough resources")
            return

        self.resources[self.turn][give_res] -= cost
        self.resources[self.turn][get_res] += 1

        self.show_message(f"{cost} {give_res} → 1 {get_res}")

    
    def check_win(self):
        vp = self.get_victory_points(self.turn)
        if vp >= 6:
            result = self.turn

            game = self.UpdateCSV(self.player1, self.player2, "Catan", result)
            game.run()

            game = self.CommonWC(self.player1, self.player2, result, self.mode, self.screen, self.movearray)
            game.run()

            return True
        return False

    def draw(self):
        font = pygame.font.Font(None, 24)

        for (q,r), resource in self.board.items():
            x, y = self.axial_to_pixel(q, r)
            img = self.tiles[resource]
            rect = img.get_rect(center=(x,y))
            self.screen.blit(img, rect)
        
        for (q,r), nums in self.title_numbers.items():
            if nums:
                x, y = self.axial_to_pixel(q, r)

                text = font.render(f"{nums[0]},{nums[1]}", True, (0, 0, 0))
                rect = text.get_rect(center=(x, y))
                self.screen.blit(text, rect)

        for pos, port in self.ports.items():
            x, y = self.axial_to_pixel(pos[0], pos[1])
            
            dx = x - self.center_x
            dy = y - self.center_y

            px = x + dx * 0.35
            py = y + dy * 0.35

            text = self.font_small.render(port, True, (255, 255, 255))
            rect = text.get_rect(center=(px, py))
            self.screen.blit(text, rect)
        
        for v, player in self.vertex_owner.items():
            x, y = self.vertices[v]
            if self.vertex_type[v] == "city":
                img = pygame.transform.scale(self.settlement_imgs[player], (40, 40))
            else:                
                img = self.settlement_imgs[player]
            rect = img.get_rect(center=(x,y))
            self.screen.blit(img, rect)
        
        for e, player in self.edge_owner.items():
            v1, v2 = self.edges[e]
            x1, y1 = self.vertices[v1]
            x2, y2 = self.vertices[v2]

            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            img = pygame.transform.rotate(self.road_imgs[player], -angle)
            rect = img.get_rect(center=((x1 + x2) / 2, (y1 + y2) / 2))
            self.screen.blit(img, rect)
        
        for v, (x, y) in self.vertices.items():
            pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 4)
        
        for e, (v1, v2) in self.edges.items():
            x1, y1 = self.vertices[v1]
            x2, y2 = self.vertices[v2]
            pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2), 2)
        
        if self.last_roll is not None:
            text = self.font_big.render(f"Roll: {self.last_roll}", True, (255, 255, 255))
            self.screen.blit(text, (450, 20))
        
        text = self.font_small.render("ROLL DICE", True, (255, 255, 255))
        self.screen.blit(text, (450, 100))

        text = self.font_small.render("END TURN", True, (255, 255, 255))
        self.screen.blit(text, (820, 150))

        text = self.font_small.render("BUILD", True, (255, 255, 255))
        self.screen.blit(text, (400, 70))

        if self.moving_robber:
            text = self.font_small.render("Move the Robber", True, (255, 0, 0))
            self.screen.blit(text, (400, 200))

        turn_text = self.font_small.render(f"Player {self.turn}'s Turn", True, (255, 255, 255))
        self.screen.blit(turn_text, (20, 20))

        y_offset = 600

        for player in [1, 2]:
            text = self.font_small.render(f"P{player}: {self.resources[player]}", True, (255, 255, 255))
            self.screen.blit(text, (50 if player == 1 else 600, y_offset))
        
        if self.build_mode:
            options = ["Road", "Settlement", "City", "Dev Card"]

            for i, opt in enumerate(options):
                text = self.font_small.render(opt, True, (0,0,0))
                self.screen.blit(text, (400, 120 + i * 50))
        
        if self.build_type:
            text = self.font_small.render(f"Building: {self.build_type}", True, (255, 255, 255))
            self.screen.blit(text, (400, 50))

        y = 650
        for player in [1, 2]:
            s = self.structures[player]
            text = self.font_small.render(f"P{player} Roads: {s['road']} Settlements: {s['settlement']} Cities: {s['city']}", True, (255, 255, 255))
            self.screen.blit(text, (50 if player == 1 else 600, y))
        
        if self.robber_pos:
            x, y = self.axial_to_pixel(self.robber_pos[0], self.robber_pos[1])
            rect = self.robber_img.get_rect(center=(x,y))
            self.screen.blit(self.robber_img, rect)

        if self.message:
            if time.time() - self.message_start_time < self.message_timer:
                text = self.font_big.render(self.message, True, (255, 255, 0))
                rect = text.get_rect(center=(500, 100))
                self.screen.blit(text, rect)
            else:
                self.message = ""

        for player in [1, 2]:
            vp = self.get_victory_points(player)
            text = self.font_small.render(f"P{player} VP: {vp}", True, (255, 255, 255))
            self.screen.blit(text, (50 if player == 1 else 600, 560))

        text = self.font_small.render("MARITIME", True, (255, 255, 255))
        self.screen.blit(text, (600, 120))

        text = self.font_small.render("PORT", True, (255, 255, 255))
        self.screen.blit(text, (600, 170))

        if self.maritime_mode:
            if not self.trade_get_mode:
                self.screen.blit(self.font_small.render("Click resource to give (4:1)", True, (255, 255, 0)), (350, 250))
            else:
                self.screen.blit(self.font_small.render("Click resource to get", True, (255,255,0)), (350, 250))
        
        if self.port_mode:
            if not self.trade_get_mode:
                self.screen.blit(self.font_small.render("Click resource to give (port trade)", True, (255, 255, 0)), (350, 300))
            else:
                self.screen.blit(self.font_small.render("Click resource to get", True, (255, 255, 0)), (350, 300))
            
        text = self.font_small.render("TRADE", True, (255, 255, 255))
        self.screen.blit(text, (600, 220))
        if self.player_trade_mode and not self.awaiting_response:
            self.screen.blit(self.font_small.render("Select GIVE resource", True, (255,255,0)), (350, 350))

        if self.awaiting_response:
            offer = self.trade_offer
            msg = f"P{self.turn} offers {offer['give']} for {offer['get']}"
            self.screen.blit(self.font_small.render(msg, True, (255,255,0)), (300, 350))

            self.screen.blit(self.font_small.render("ACCEPT", True, (0,255,0)), (400, 400))
            self.screen.blit(self.font_small.render("REJECT", True, (255,0,0)), (550, 400))
        
        if self.turn == 1:
            pygame.draw.rect(self.screen, (255, 0, 0), (50, 150, 120, 40))
            text = self.font_small.render("RESIGN", True, (255, 255, 255))
            self.screen.blit(text, (60, 160))

        if self.turn == 2:
            pygame.draw.rect(self.screen, (255, 0, 0), (830, 150, 120, 40))
            text = self.font_small.render("RESIGN", True, (255, 255, 255))
            self.screen.blit(text, (840, 160))
        


    def run(self):
        background = pygame.image.load("CatanBackground.png")
        background = pygame.transform.scale(background, (1000,700))

        running = True
        while running:
            self.screen.blit(background, (0,0))
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()


                    if 600 <= mx <= 750 and 120 <= my <= 160:
                        if self.phase == "normal" and self.has_rolled:
                            self.maritime_mode = True
                            self.port_mode = False
                            self.trade_get_mode = False
                            self.trade_give = None
                            self.show_message("Maritime Trade")
                        continue

                    if 600 <= mx <= 750 and 170 <= my <= 210:
                        if self.phase == "normal" and self.has_rolled:

                            has_any_port = False
                            for res in ["wood","brick","wool","wheat","ore"]:
                                if self.has_port(self.turn, res):
                                    has_any_port = True
                            if self.has_port(self.turn, "3:1"):
                                has_any_port = True

                            if has_any_port:
                                self.port_mode = True
                                self.maritime_mode = False
                                self.trade_get_mode = False
                                self.trade_give = None
                                self.show_message("Port Trade")
                            else:
                                self.show_message("No port access")

                        continue

                    if 600 <= mx <= 750 and 220 <= my <= 260:
                        if self.phase == "normal" and self.has_rolled:
                            self.player_trade_mode = True
                            self.trade_get_mode = False
                            self.trade_give = None
                            self.trade_offer = None
                        continue

                    if self.moving_robber:
                        tile = self.get_clicked_tile((mx, my))
                        if tile is not None:
                            self.robber_pos = tile
                            self.moving_robber = False

                            self.steal_from_opponent(tile)
                        continue

                    if self.turn == 1 and 50 <= mx <= 170 and 150 <= my <= 190:
                        resign = self.Resign(
                            self.player1,
                            self.player2,
                            None,
                            self.screen,
                            self.mode,
                            2,  
                            self.movearray
                        )
                        resign.run()

                    if self.turn == 2 and 830 <= mx <= 950 and 150 <= my <= 190:
                        resign = self.Resign(
                            self.player1,
                            self.player2,
                            None,
                            self.screen,
                            self.mode,
                            1, 
                            self.movearray
                        )
                        resign.run()

                    v = self.get_clicked_vertex((mx, my))
                    if v is not None:
                        if self.phase == "setup" and self.setup_stage == "settlement":
                            if self.can_place_settlement(v):
                                if self.structures[self.turn]["settlement"] > 0:
                                    self.vertex_owner[v] = self.turn
                                    self.vertex_type[v] = "settlement"
                                    self.structures[self.turn]["settlement"] -= 1

                                    self.last_settlement = v
                                    self.setup_stage = "road"

                                self.last_settlement = v
                                self.setup_stage = "road"
                            
                            continue

                        if self.phase == "normal" and self.build_mode and self.build_type == "Settlement":
                            if self.can_place_settlement(v) and self.can_afford(self.turn, "Settlement"):
                                if self.structures[self.turn]["settlement"] > 0:
                                    self.pay_cost(self.turn, "Settlement")
                                    self.vertex_owner[v] = self.turn
                                    self.vertex_type[v] = "settlement"
                                    self.structures[self.turn]["settlement"] -= 1
                                    if self.check_win():
                                        return
                            continue

                        if self.phase == "normal" and self.build_mode and self.build_type == "City":
                            if v in self.vertex_owner and self.vertex_owner[v] == self.turn:
                                if self.vertex_type[v] == "settlement":
                                    if self.structures[self.turn]["city"] > 0 and self.can_afford(self.turn, "City"):
                                        self.pay_cost(self.turn, "City")
                                        self.vertex_type[v] = "city"
                                        self.structures[self.turn]["city"] -= 1
                                        self.structures[self.turn]["settlement"] += 1
                                        if self.check_win():
                                            return
                            continue

                        if self.phase == "normal" and self.build_mode and self.build_type == "Dev Card":
                            if self.can_afford(self.turn, "Dev Card"):
                                self.pay_cost(self.turn, "Dev Card")
                                self.play_dev_card()
                
                    e = self.get_clicked_edge((mx, my))
                    if e is not None:
                        if self.phase == "setup" and self.setup_stage == "road":
                            v1, v2 = self.edges[e]

                            if self.last_settlement in (v1, v2):
                                self.edge_owner[e] = self.turn
                                self.setup_moves[self.turn] += 1

                                self.turn = 3 - self.turn
                                self.setup_stage = "settlement"

                                if self.setup_moves[1] == 1 and self.setup_moves[2] == 1:
                                    self.phase = "normal"

                        if self.phase == "normal" and self.build_mode and self.build_type == "Road":
                            if self.can_place_road(e):
                                if self.free_road:
                                    self.edge_owner[e] = self.turn
                                    self.structures[self.turn]["road"] -= 1
                                    self.free_road = False
                                elif self.can_afford(self.turn, "Road"):
                                    if self.structures[self.turn]["road"] > 0:
                                        self.pay_cost(self.turn, "Road")
                                        self.edge_owner[e] = self.turn
                                        self.structures[self.turn]["road"] -= 1

                                length = self.get_longest_road(self.turn)

                                if length >= 4 and length > self.longest_road_length:
                                    self.longest_road_length = length
                                    self.longest_road_owner = self.turn
                                    self.show_message(f"Player {self.turn} gets Longest Road!")
                                if self.check_win():
                                    return
                            continue

                    if 450 <= mx <= 550 and 100 <= my <= 150:
                        if self.phase == "normal" and not self.has_rolled:
                            roll = self.roll_dice()
                            self.last_roll = roll
                            if roll == 7:
                                for player in [1, 2]:
                                    self.discard_half(player)
                                self.moving_robber = True
                            else:
                                self.distribute_resources(roll)

                            self.has_rolled = True
                            self.turn_phase = "action"
                            continue

                    if 820 <= mx <= 940 and 150 <= my <= 200:
                        if self.phase == "normal" and self.has_rolled:
                            self.turn = 3 - self.turn
                            self.has_rolled = False
                            self.turn_phase = "roll"
                            continue
                    
                    if 400 <= mx <= 520 and 70 <= my <= 120:
                        if self.phase == "normal" and self.has_rolled:
                            self.build_mode = not self.build_mode
                            continue
                    

                    if self.build_mode:
                        for i, opt in enumerate(["Road", "Settlement", "City", "Dev Card"]):
                            if 350 <= mx <= 550 and 110 + i * 50 <= my <= 150 + i * 50:
                                if opt == "Dev Card":
                                    if self.can_afford(self.turn, "Dev Card"):
                                        self.pay_cost(self.turn, "Dev Card")
                                        self.play_dev_card()
                                else:
                                    self.build_type = opt
                                break

                    resources = ["wood", "brick", "wool", "wheat", "ore"]

                    if self.maritime_mode:

                        handled = False

                        for i, res in enumerate(resources):
                            if 50 + i*100 <= mx <= 130 + i*100 and 600 <= my <= 630:

                                handled = True

                                if not self.trade_get_mode:
                                    self.trade_give = res
                                    self.trade_get_mode = True
                                    self.show_message(f"Give: {res}")

                                else:
                                    give = self.trade_give
                                    get = res

                                    self.maritime_trade(give, get)

                                    self.maritime_mode = False
                                    self.trade_get_mode = False
                                    self.trade_give = None

                                break

                        if not handled and not self.trade_get_mode:
                            self.maritime_mode = False


                    if self.port_mode:

                        handled = False

                        for i, res in enumerate(resources):
                            if 50 + i*100 <= mx <= 130 + i*100 and 600 <= my <= 630:

                                handled = True

                                if not self.trade_get_mode:
                                    self.trade_give = res
                                    self.trade_get_mode = True
                                    self.show_message(f"Give: {res}")

                                else:
                                    give = self.trade_give
                                    get = res

                                    self.port_trade(give, get)

                                    self.port_mode = False
                                    self.trade_get_mode = False
                                    self.trade_give = None

                                break

                        if not handled and not self.trade_get_mode:
                            self.port_mode = False




                    if self.player_trade_mode and not self.awaiting_response:

                        handled = False
                        resources = ["wood","brick","wool","wheat","ore"]

                        for i, res in enumerate(resources):
                            if 50 + i*100 <= mx <= 130 + i*100 and 600 <= my <= 630:

                                handled = True

                                if not self.trade_get_mode:
                                    if self.resources[self.turn][res] <= 0:
                                        self.show_message("Not enough resource")
                                        break

                                    self.trade_give = res
                                    self.trade_get_mode = True
                                    self.show_message(f"Give: {res}")

                                else:
                                    self.trade_offer = {
                                        "give": self.trade_give,
                                        "get": res,
                                        "from": self.turn,
                                        "to": 3 - self.turn
                                    }

                                    self.awaiting_response = True
                                    self.player_trade_mode = False
                                    self.trade_get_mode = False
                                    self.trade_give = None

                                    self.show_message("Waiting for opponent")

                                break

                        if not handled and not self.trade_get_mode:
                            self.player_trade_mode = False

                    
                    if self.awaiting_response:

                        if 400 <= mx <= 480 and 400 <= my <= 440:
                            offer = self.trade_offer
                            giver = offer["from"]
                            receiver = offer["to"]

                            give_res = offer["give"]
                            get_res = offer["get"]

                            if self.resources[receiver][get_res] > 0:

                                self.resources[giver][give_res] -= 1
                                self.resources[receiver][give_res] += 1

                                self.resources[receiver][get_res] -= 1
                                self.resources[giver][get_res] += 1

                                self.show_message("Trade completed")

                            else:
                                self.show_message("Opponent lacks resource")

                            self.awaiting_response = False
                            self.trade_offer = None

                        elif 550 <= mx <= 650 and 400 <= my <= 440:
                                self.show_message("Trade rejected")
                                self.awaiting_response = False
                                self.trade_offer = None

                        continue
 

                    
            pygame.display.flip()

        pygame.quit()
