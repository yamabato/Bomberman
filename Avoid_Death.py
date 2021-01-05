#encoding: utf-8
import os
import random

from Model import Model

class Avoid_Death(Model):
    def init(self):
        self.IMG_FILE = os.getcwd() + "/img/mark_face_tere.png"
        self.PLACE_BOMB_RATE = 0.05

    def calc_explosion_place(self,board,timing):
        place = [[0 for j in range(self.SIZE)] for i in range(self.SIZE)]

        for y in range(self.SIZE):
            for x in range(self.SIZE):
                block = board[y][x]
                if block == self.BOMB:
                    for d in self.DIRECTIONS:
                        ax,ay = d
                        for i in range(self.EXPLOSION_RANGE):
                            x2,y2 = x+ax, y+ay
                            if x2 < 0 or x2 >= self.SIZE or y2 < 0 or y2 >= self.SIZE:
                                break
                            if board[y2][x2] == self.AISLE:
                                place[y2][x2] = timing[y][x]
                            else:
                                break
        return place
 
    def avoid(self,pos,board,timing,direction):
        x,y = pos
        x2,y2 = x+self.DIRECTIONS[direction][0], y+self.DIRECTIONS[direction][1]
        
        if board[y][x] == self.BOMB: return True

        block = board[y2][x2]
        if block in self.KILL_BLOCK: return False
        if timing[y2][x2] != 0: return False

        explosion_place = self.calc_explosion_place(board,timing)
        if explosion_place[y2][x2] > 0: return False

        return True

    def move(self,board,timing,players,count):
        commands = []
        pos = players[self.ID]
        for n in range(4):
            if self.can_go(pos,board,players,n):
                if self.avoid(pos,board,timing,n):
                    commands.append(n)

        if not commands: return -1

        if random.random() < self.PLACE_BOMB_RATE: return 4

        return random.choice(commands)



