#encoding: utf-8

from tkinter import *

class Maker:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 900
        self.TITLE = "AIメーカー"

        self.tk = Tk()
        self.tk.geometry("{0}x{1}".format(self.WIDTH,self.HEIGHT))
        self.tk.title(self.TITLE)

    def main(self):
        while True:
            self.tk.update()

maker = Maker()
maker.main()
