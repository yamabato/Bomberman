#encoding: utf-8
import os
import random

from Model import Model

class Avoid_Death(Model):
    def init(self):
        imgs = ["hamster","ninja","mark_face_odoroki","engiri_mark","food_fish_hiraki","nature_stone_iwa"]
        img = random.choice(imgs)
        self.IMG_FILE = os.getcwd() + "/img/" + img+".png"
        self.PLACE_BOMB_RATE = 0.01

        self.LAST_MOVE = [0,0]
        self.LAST_BOARD = []
        self.LAST_TIMING = []
        self.LAST_EXPLOSION_PLACE = []

    def calc_explosion_place(self,board,timing):
        place = [[0 for j in range(self.SIZE)] for i in range(self.SIZE)]

        for y in range(self.SIZE):
            for x in range(self.SIZE):
                block = board[y][x]
                if block == self.BOMB:
                    for d in self.DIRECTIONS:
                        ax,ay = d
                        x2,y2 = x,y
                        for i in range(self.EXPLOSION_RANGE):
                            x2,y2 = x2+ax, y2+ay
                            if x2 < 0 or x2 >= self.SIZE or y2 < 0 or y2 >= self.SIZE:
                                break
                            if board[y2][x2] == self.AISLE:
                                place[y2][x2] = timing[y][x]
                            else:
                                break
        return place
 
    def eval_move(self,pos,board,timing,explosion_place,direction):
        x,y = pos
        x2,y2 = x+self.DIRECTIONS[direction][0], y+self.DIRECTIONS[direction][1]
        
        block = board[y2][x2]
        if block in self.KILL_BLOCK: return -1
        if self.LAST_BOARD and self.LAST_BOARD[y2][x2] in self.KILL_BLOCK: return -1
        if self.LAST_TIMING and self.LAST_TIMING[y2][x2] > 0: return 3

        if board[y][x] == self.BOMB:
            if board[y2][x2] == self.AISLE:
                space = 0
                for d in self.DIRECTIONS:
                    x3,y3 = x2 + d[0], y2 + d[1]
                    if x3 >= 0 and x3 < self.SIZE and y3 >= 0 and y3 < self.SIZE:
                        if board[y3][x3] == self.AISLE: space += 1

                if space >= 2: return 20
                return 18
            return 15


        result = self.check_explosion_place(pos,(x2,y2),board,explosion_place)
        if result is not None: return result

        if self.LAST_EXPLOSION_PLACE:
            result = self.check_explosion_place(pos,(x2,y2),board,self.LAST_EXPLOSION_PLACE)
        if result is not None: return result // 2

        space = 0
        for d in self.DIRECTIONS[:-1]:
            x3,y3 = x2 + d[0], y2 + d[1]
            if x3 >= 0 and x3 < self.SIZE and y3 >= 0 and y3 < self.SIZE:
                if board[y3][x3] == self.AISLE: space += 1

        if space >= 2: return 10
        return 5

    def check_explosion_place(self,pos,pos2,board,explosion_place):
        x,y = pos
        x2,y2 = pos2
        if explosion_place[y][x]:
            if not explosion_place[y2][x2]: return 25
            if explosion_place[y2][x2] > explosion_place[y][x]: return 15

            nearest_bomb = self.find_nearest_bomb(board,pos)
            if nearest_bomb[1][0] != -1:
                bx, by = nearest_bomb[1]
                if (x2 - bx)**2 + (y2 - by)**2 > (x - bx)**2 + (y - by)**2: return 15
        if explosion_place[y2][x2]: return 2

        return None

 
    def find_nearest_bomb(self,board,pos):
        px,py = pos
        bomb = [float("inf"),(-1,-1)]

        for y in range(self.SIZE):
            for x in range(self.SIZE):
                block = board[y][x]
                if block == self.BOMB:
                    distance = (px - x) ** 2 + (py - y) ** 2
                    if distance < bomb[0]: bomb = [distance, (x,y)]
        return bomb

    def avoid(self,board,timing,players,count):
        command = None
        commands = []
        pos = players[self.ID]
        explosion_place = self.calc_explosion_place(board,timing)

        for n in range(-1,4):
            if self.can_go(pos,board,players,n):
                v =  self.eval_move(pos,board,timing,explosion_place,n)
                commands.append([n,v])

                if n == -1 and v>0 and self.LAST_MOVE[0] != -1 and self.LAST_MOVE[-1] == -1:
                    command = -1
                    break

        if not commands: commands.append([-1,0])
        if command is None and random.random() < self.PLACE_BOMB_RATE: command = 4

        random.shuffle(commands)
        commands.sort(key=lambda x:x[1])

        if command is None: command = commands[-1][0]

        print self.ID, commands

        self.LAST_BOARD = board
        self.LAST_TIMING = timing
        self.LAST_EXPLOSION_PLACE = explosion_place
            
        return command,commands

    def move(self,board,timing,players,count):
        command,commands = self.avoid(board,timing,players,count)
        self.LAST_MOVE = self.LAST_MOVE[1:] + [command]

        if command is None:
            if random.random() < self.PLACE_BOMB_RATE: return 4
            else: return commands[-1][0]
        return command

