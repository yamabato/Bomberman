#ecoding: utf-8
import os
import random


class Model:
    def __init__(self,tk,player_id,FPS,SIZE,UPDATE_TICK,block_id,SPEED,EXPLOSION_LEFT,BOMB_EXPLODE_TIME,EXPLOSION_RANGE,CAN_GO,KILL_BLOCK):
        self.FPS = FPS
        self.ID = player_id

        self.AISLE = block_id["AISLE"]
        self.BRICK = block_id["BRICK"]
        self.STONE = block_id["STONE"]
        self.PLAYER1 = block_id["PLAYER1"]
        self.PLAYER2 = block_id["PLAYER2"]
        self.PLAYER3 = block_id["PLAYER3"]
        self.PLAYER4 = block_id["PLAYER4"]
        self.BOMB = block_id["BOMB"]
        self.EXPLOSION = block_id["EXPLOSION"]
        self.EXPLOSION_GROUND = block_id["EXPLOSION_GROUND"]
        
        self.UPDATE_TICK = UPDATE_TICK
        self.SIZE = SIZE
        self.EXPLOSION_LEFT = EXPLOSION_LEFT
        self.BOMB_EXPLODE_TIME = BOMB_EXPLODE_TIME
        self.EXPLOSION_RANGE = EXPLOSION_RANGE

        self.CAN_GO = CAN_GO
        self.KILL_BLOCK = KILL_BLOCK

        self.IMG_FILE = os.getcwd() + "/img/" + "mark_face_smile.png"

        self.tk = tk

        self.ARROW_COMMAND = {
            "Up": 0,
            "Left": 1,
            "Right": 2,
            "Down": 3,
            "space": 4,
        }

        self.DIRECTIONS = [
            (0,-1),
            (-1,0),
            (1,0),
            (0,1),
            (0,0),
        ]

        self.init()
    
    def init(self):
        #ここに好きな初期化関数をかく
        pass
    
    def can_go(self,pos,board,players,direction):
        x,y = pos
        x2,y2 = x+self.DIRECTIONS[direction][0], y+self.DIRECTIONS[direction][1]
        
        if x2 < 0 or x2 >= self.SIZE or y2 < 0 or y2 >= self.SIZE:
            return False

        if board[y2][x2] in self.CAN_GO:
            for n in range(4):
                if n == self.ID: continue

                px, py = players[n]
                if px == x2 and py == y2:
                    return False
            return True

    def move(self,board,timing,players,count):
       return -1


