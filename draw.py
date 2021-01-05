#encoding: utf-8
from tkinter import *
import random
import time
import copy

from PIL import Image, ImageTk, ImageChops

from board import Board
from Model import Model
from Avoid_Death import Avoid_Death
from Human import Human

class Game:
    def __init__(self,fps,players):
        self.tk = Tk()
        self.tk.title("Bomberman")

        self.FPS = fps
        self.WAIT = 1.0 / self.FPS
        self.UPDATE_TICK = 6

        self.board = Board(self.FPS)

        self.RANDOM_CONST = random.random()

        self.BLOCK_SIZE = 50
        self.BG_CLR = "#98d98e"
        self.BRICK_CLR = "#bb5548"
        self.CEMENT_CLR = "#dcdddd"
        self.STONE_CLR = "#9fa0a0"
                
        self.BOMB_IMG_NAME = "img/bomb.png"
        self.NUKE_IMG_NAME = "img/nuke.png"
        self.EXPLOSION_IMG_NAME = "img/bomb_explode.png"
        self.EXPLOSION_GROUND_IMG_NAME = "img/bomb_explode_ground.png"
        self.BOMB_IMG = ImageTk.PhotoImage(Image.open(self.BOMB_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.BOMB_IMG_mini = ImageTk.PhotoImage(Image.open(self.BOMB_IMG_NAME).resize((int(self.BLOCK_SIZE*0.9),int(self.BLOCK_SIZE*0.9))))
        self.NUKE_IMG = ImageTk.PhotoImage(Image.open(self.NUKE_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.EXPLOSION_IMG = ImageTk.PhotoImage(Image.open(self.EXPLOSION_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.EXPLOSION_GROUND_IMG = ImageTk.PhotoImage(Image.open(self.EXPLOSION_GROUND_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.BOMB_IMGs = [self.BOMB_IMG]
        self.EXPLOSION_IMGs = [self.EXPLOSION_IMG,self.EXPLOSION_GROUND_IMG]

        self.AISLE = self.board.AISLE
        self.STONE = self.board.STONE
        self.BRICK = self.board.BRICK
        self.PLAYER1 = self.board.PLAYER1
        self.PLAYER2 = self.board.PLAYER2
        self.PLAYER3 = self.board.PLAYER3
        self.PLAYER4 = self.board.PLAYER4
        self.BOMB = self.board.BOMB
        self.EXPLOSION = self.board.EXPLOSION
        self.EXPLOSION_GROUND = self.board.EXPLOSION_GROUND

        self.SPEED = self.board.SPEED
        self.EXPLOSION_LEFT = self.board.EXPLOSION_LEFT
        self.BOMB_EXPLODE_TIME = self.board.BOMB_EXPLODE_TIME
        self.EXPLOSION_RANGE = self.board.EXPLOSION_RANGE
        self.CAN_GO = self.board.CAN_GO
        self.KILL_BLOCK = self.board.KILL_BLOCK

        self.SIZE = self.board.SIZE
        self.WINDOW_SIZE = self.SIZE * self.BLOCK_SIZE

        self.clock = 0
        self.end = False

        self.tk.geometry("{0}x{0}".format(self.WINDOW_SIZE))

        self.canvas = Canvas(self.tk,width=self.WINDOW_SIZE,height=self.WINDOW_SIZE)
        self.canvas.pack()
        self.tk.bind("<KeyPress>",lambda e: self.set_key(e))

        self.ARROW_DIRECTION = {
            "Up": 0,
            "Left": 1,
            "Right": 2,
            "Down": 3,
        }
        
        self.key = 0

        block_id = {
            "AISLE": self.AISLE,
            "BRICK": self.BRICK,
            "STONE": self.STONE,
            "PLAYER1": self.PLAYER1,
            "PLAYER2": self.PLAYER2,
            "PLAYER3": self.PLAYER3,
            "PLAYER4": self.PLAYER4,
            "BOMB": self.BOMB,
            "EXPLOSION": self.EXPLOSION,
            "EXPLOSION_GROUND": self.EXPLOSION_GROUND,
        }

        self.PLAYERS = [players[n](self.tk,n,self.FPS,self.SIZE,self.UPDATE_TICK,block_id,self.SPEED,self.EXPLOSION_LEFT,self.BOMB_EXPLODE_TIME,self.EXPLOSION_RANGE,self.CAN_GO,self.KILL_BLOCK) for n in range(4)]

        self.PLAYER1_IMG_NAME = self.PLAYERS[0].IMG_FILE
        self.PLAYER2_IMG_NAME = self.PLAYERS[1].IMG_FILE
        self.PLAYER3_IMG_NAME = self.PLAYERS[2].IMG_FILE
        self.PLAYER4_IMG_NAME = self.PLAYERS[3].IMG_FILE
        self.PLAYER1_IMG = ImageTk.PhotoImage(Image.open(self.PLAYER1_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.PLAYER2_IMG = ImageTk.PhotoImage(Image.open(self.PLAYER2_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.PLAYER3_IMG = ImageTk.PhotoImage(Image.open(self.PLAYER3_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.PLAYER4_IMG = ImageTk.PhotoImage(Image.open(self.PLAYER4_IMG_NAME).resize((self.BLOCK_SIZE,self.BLOCK_SIZE)))
        self.PLAYER_IMGs = [self.PLAYER1_IMG,self.PLAYER2_IMG,self.PLAYER3_IMG,self.PLAYER4_IMG]

        self.draw()
    
    def set_key(self,e):
        self.key = e.keysym
        if self.key == "q": self.end = True

    def block_draw(self):
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                block = self.board.board[y][x]

                if block == self.AISLE:
                    self.canvas.create_rectangle(x*self.BLOCK_SIZE,y*self.BLOCK_SIZE,(x+1)*self.BLOCK_SIZE,(y+1)*self.BLOCK_SIZE,fill=self.BG_CLR,width=0)
                elif block == self.STONE:
                    self.canvas.create_rectangle(x*self.BLOCK_SIZE,y*self.BLOCK_SIZE,(x+1)*self.BLOCK_SIZE,(y+1)*self.BLOCK_SIZE,fill=self.STONE_CLR,outline="black",width=2)
                elif block == self.BRICK:
                    for i in  range(3):
                        self.canvas.create_rectangle(
                                x*self.BLOCK_SIZE,
                                y*self.BLOCK_SIZE+(self.BLOCK_SIZE//3)*i,
                                x*self.BLOCK_SIZE+(self.BLOCK_SIZE//3)*3,
                                y*self.BLOCK_SIZE+(self.BLOCK_SIZE//3)*(i+1),
                                fill=self.BRICK_CLR,outline=self.CEMENT_CLR,width=1)

    def object_draw(self):
        bomb_size_gap = self.BLOCK_SIZE//20 if (self.clock//30)%2==0 else 0
        bomb_img = self.BOMB_IMG_mini if (self.clock//30)%2==0 else self.BOMB_IMG
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                block = self.board.board[y][x]
                if block == self.BOMB:
                    self.canvas.create_rectangle(x*self.BLOCK_SIZE,y*self.BLOCK_SIZE,(x+1)*self.BLOCK_SIZE,(y+1)*self.BLOCK_SIZE,fill=self.BG_CLR,width=0)
                    self.canvas.create_image(
                            x*self.BLOCK_SIZE+self.BLOCK_SIZE//2+bomb_size_gap,y*self.BLOCK_SIZE+self.BLOCK_SIZE//2+bomb_size_gap,
                            image=bomb_img)
                elif block >= self.EXPLOSION and block <= self.EXPLOSION_GROUND:
                    self.canvas.create_image(x*self.BLOCK_SIZE+self.BLOCK_SIZE//2,y*self.BLOCK_SIZE+self.BLOCK_SIZE//2,image=self.EXPLOSION_IMGs[block-self.EXPLOSION])

    def player_draw(self):
        for n in range(4):
            x,y = self.board.PLAYER_POS[n]
            if x == -1: continue
            self.canvas.create_image(x*self.BLOCK_SIZE+self.BLOCK_SIZE//2,y*self.BLOCK_SIZE+self.BLOCK_SIZE//2,image=self.PLAYER_IMGs[n])

    def draw(self):
        self.canvas.delete("all")
        self.block_draw()
        self.object_draw()
        self.player_draw()
        self.tk.update()

        self.clock += 1

 
    def update(self):
        self.board.update()
        if self.clock % (self.FPS // self.UPDATE_TICK)== 0:
            for n in range(4):
                if self.board.PLAYER_POS[n][0] == -1: continue
                board = copy.deepcopy(self.board.board)
                timing = copy.deepcopy(self.board.timing)
                players = copy.deepcopy(self.board.PLAYER_POS)

                player = self.PLAYERS[n]
                try:
                    command = player.move(board,timing,players,self.clock)
                except:
                    print "ERROR AT PLAYER {0}({1}) THINKING".format(n+1,player.__class__.__name__)  
                    command = -1
                if command == -1: pass
                elif command >= 0 and command <= 4: self.board.move(command,n+1)

        self.draw()
        self.tk.update()

    def game(self):
        while True:
            if self.end: return
            t = time.time()

            self.update()
            
            now = time.time()
            diff = now - t
            if diff < self.WAIT:
                time.sleep(self.WAIT - diff)
                        

FPS = 60

players = [
    Avoid_Death,
    Avoid_Death,
    Avoid_Death,
    Model,
][:4]
game = Game(FPS,players)
game.game()

