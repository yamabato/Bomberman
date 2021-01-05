#encoding: utf-8
from decimal import Decimal
import subprocess
import random
import math

class Board:
    SIZE = 15
    def __init__(self,fps):
        self.FPS = fps

        #0:無 1:壁 2:レンガ
        self.AISLE = 0
        self.STONE = 1
        self.BRICK = 2

        self.PLAYER1 = 3
        self.PLAYER2 = 4
        self.PLAYER3 = 5
        self.PLAYER4 = 6

        self.BOMB = 7
        self.EXPLOSION = 8
        self.EXPLOSION_GROUND = 9

        self.EXPLOSION_LEFT = 1 * self.FPS
        self.BOMB_EXPLODE_TIME = 1 * self.FPS
        self.EXPLOSION_RANGE = 3

        self.RATE = 0.5
        self.RATE = 0.1
        self.init_board()

        self.SPEED = 1
        self.CAN_GO = [self.AISLE, self.EXPLOSION_GROUND, self.EXPLOSION]
        self.KILL_BLOCK = [self.EXPLOSION, self.EXPLOSION_GROUND]
        self.PLAYER_POS = [
            [0,0],
            [self.SIZE-1,0],
            [0,self.SIZE-1],
            [self.SIZE-1,self.SIZE-1]
        ]
        self.DIRECTION = [
            (Decimal(0),Decimal(-self.SPEED), Decimal(0),Decimal(-1+self.SPEED)),
            (Decimal(-self.SPEED),Decimal(0), Decimal(-1+self.SPEED),Decimal(0)),
            (Decimal(self.SPEED),Decimal(0),  Decimal(0),Decimal(0)),
            (Decimal(0),Decimal(self.SPEED),  Decimal(0),Decimal(0)),
        ]
        self.TOUCH_BLOCKS = [
            (lambda x: int(x), lambda x: int(x)),
            (lambda x: int(x+Decimal(0.5)), lambda x: int(x)),
            (lambda x: int(x), lambda x: int(x+Decimal(0.5))),
            (lambda x: int(x+Decimal(0.5)), lambda x:int(x+Decimal(0.5))),
        ]

    def init_board(self):
        self.board = [[self.STONE if i*j%2==1 else (self.BRICK if random.random()<=self.RATE else self.AISLE) for j in range(self.SIZE)] for i in range(self.SIZE)]
        self.timing = [[0 for j in range(self.SIZE)] for i in range(self.SIZE)]

        self.board[0][0] = self.AISLE
        self.board[0][self.SIZE-1] = self.AISLE
        self.board[self.SIZE-1][0] = self.AISLE
        self.board[self.SIZE-1][self.SIZE-1] = self.AISLE

        self.board[0][1] = self.AISLE
        self.board[1][0] = self.AISLE
        self.board[0][self.SIZE-2] = self.AISLE
        self.board[1][self.SIZE-1] = self.AISLE
        self.board[self.SIZE-2][0] = self.AISLE
        self.board[self.SIZE-1][1] = self.AISLE
        self.board[self.SIZE-2][self.SIZE-1] = self.AISLE
        self.board[self.SIZE-1][self.SIZE-2] = self.AISLE


    def move(self,direction,player):
        """
         0
        1P2
         3
        4 爆弾設置
        player 1~4
        """

        place = self.PLAYER_POS[player - 1]
        if place[0] == -1:
            return

        block = -1

        if direction >= 0 and direction <= 3:
            x2,y2 = Decimal(place[0]) + self.DIRECTION[direction][0],Decimal(place[1]) + self.DIRECTION[direction][1]
            x2_int,y2_int = self.pos_to_int(x2+self.DIRECTION[direction][2]),self.pos_to_int(y2+self.DIRECTION[direction][3])

            if x2_int >= 0 and x2 < self.SIZE and y2_int >= 0 and y2 < self.SIZE:
                block = self.board[y2_int][x2_int]
                if block in self.CAN_GO and not self.exist_player(x2_int,y2_int):
                    self.PLAYER_POS[player - 1] = [int(x2),int(y2)]

        elif direction == 4:
            x,y = self.pos_to_int(place[0]),self.pos_to_int(place[1])
            self.board[y][x] = self.BOMB
            self.timing[y][x] = self.BOMB_EXPLODE_TIME

    def exist_player(self,x,y):
        count = 1
        for n in range(4):
            px,py = self.PLAYER_POS[n]
            if x == px and y == py: count -= 1

        if count <= 0:
            return True
        return False

    def update(self):
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                block = self.board[y][x]
                t = self.timing[y][x]

                if t == 0:
                    if block == self.BOMB:
                        self.explode(x,y)
                    elif block in self.KILL_BLOCK:
                        self.board[y][x] = self.AISLE
                else:
                    self.timing[y][x] -= 1

        for n in range(4):
            x,y = self.PLAYER_POS[n]
            if x == -1:
                continue

            touch_blocks = set([(int(d[0](x)),int(d[1](y))) for d in self.TOUCH_BLOCKS])

            for t in touch_blocks:
                x2,y2 = t
                if self.board[y2][x2] in self.KILL_BLOCK:
                    self.PLAYER_POS[n] = [-1, -1]
                    break

    def explode(self,x,y):
        subprocess.Popen(["afplay","sound/bomb.mp3"])
        self.board[y][x] = self.EXPLOSION_GROUND
        self.timing[y][x] = self.EXPLOSION_LEFT

        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        for d in directions:
            x2,y2 = x,y
            for i in range(self.EXPLOSION_RANGE):
                x2 += d[0]
                y2 += d[1]

                if x2 >= self.SIZE or x2 < 0: break
                if y2 >= self.SIZE or y2 < 0: break
                
                block = self.board[y2][x2]
                if block == self.AISLE:
                    self.set_explosion(x2,y2)
                elif block in self.KILL_BLOCK:
                    self.timing[y2][x2] = self.EXPLOSION_LEFT
                elif block == self.BOMB:
                    self.set_explosion(x2,y2)
                    self.explode(x2,y2)
                elif block == self.BRICK:
                    self.set_explosion(x2,y2)
                    break
                else: break

    def set_explosion(self,x,y):
        self.board[y][x] = self.EXPLOSION
        self.timing[y][x] = self.EXPLOSION_LEFT

    def pos_to_int(self,v):
        return int(math.ceil(v))

                

