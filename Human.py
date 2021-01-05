#encoding: utf-8
from tkinter import *
from tkinter import filedialog
import os

from Model import Model

class Human(Model):
    def init(self):

        tk = Tk()
        tk.withdraw()
        self.IMG_FILE = ""
        self.choice_img()

        self.key = ""
        self.tk.bind("<KeyPress>",lambda e: self.set_key(e.keysym))

    def choice_img(self):
        tk = Tk()
        tk.withdraw()
        file_type = [("","*.png")]

        file_name = ""

        while not file_name:
            file_name = filedialog.askopenfilename(filetypes=file_type, initialdir=os.getcwd()+"/img/")
        self.IMG_FILE = file_name

    def set_key(self,k):
        self.key = k

    def move(self,board,timing,players,count):
        command = -1
        if self.key in self.ARROW_COMMAND:
            command = self.ARROW_COMMAND[self.key]
        self.key = ""
        return command
