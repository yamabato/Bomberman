#encoding: utf-8
import random
import subprocess

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

        self.CAN_GO = [self.AISLE, self.EXPLOSION_GROUND, self.EXPLOSION]
        self.KILL_BLOCK = [self.EXPLOSION, self.EXPLOSION_GROUND]

        self.EXPLOSION_LEFT = 1 * self.FPS
        self.BOMB_EXPLODE_TIME = 2 * self.FPS
        self.EXPLOSION_RANGE = 3

        RATE = 0.5
        RATE = 0.2
        self.board = [[self.STONE if i*j%2==1 else (self.BRICK if random.random()<=RATE else self.AISLE) for j in range(self.SIZE)] for i in range(self.SIZE)]
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

        self.PLAYER_POS = [
            [0,0],
            [0,self.SIZE-1],
            [self.SIZE-1,0],
            [self.SIZE-1,self.SIZE-1]
        ]

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
        if direction == 0:
            if place[1] > 0:
                block = self.board[place[1]-1][place[0]]
                if block in self.CAN_GO and not self.exist_player(place[0],place[1]-1):
                    self.PLAYER_POS[player - 1] = [place[0],place[1]-1]
        elif direction == 1:
            if place[0] > 0:
                block = self.board[place[1]][place[0]-1]
                if block in self.CAN_GO and not self.exist_player(place[0]-1,place[1]):
                    self.PLAYER_POS[player - 1] = [place[0]-1,place[1]]
        elif direction == 2:
            if place[0] < self.SIZE - 1:
                block = self.board[place[1]][place[0]+1]
                if block in self.CAN_GO and not self.exist_player(place[0]+1,place[1]):
                    self.PLAYER_POS[player - 1] = [place[0]+1,place[1]]
        elif direction == 3:
            if place[1] < self.SIZE - 1:
                block = self.board[place[1]+1][place[0]]
                if block in self.CAN_GO and not self.exist_player(place[0],place[1]+1):
                    self.PLAYER_POS[player - 1] = [place[0],place[1]+1]
        elif direction == 4:
            self.board[place[1]][place[0]] = self.BOMB
            self.timing[place[1]][place[0]] = self.BOMB_EXPLODE_TIME

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
            if self.board[y][x] in self.KILL_BLOCK:
                self.PLAYER_POS[n] = [-1, -1]

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

                

