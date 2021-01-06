#encoding: utf-8
import os
import random

from Model import Model

class RandomWalk(Model):
    def init(self):
        self.IMG_FILE = os.getcwd() + "/img/mark_face_tere.png"

    def move(self,board,timing,players,count):
        commands = []
        for d in range(4):
            if self.can_go(players[self.ID],board,players,d):
                commands.append(d)

        if commands: return random.choice(commands)
        return -1
 
