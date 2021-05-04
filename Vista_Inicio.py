from tkinter import *

class Inicio():
    def __init__(self, frame, w, h):
        self.frame = frame
        
        self.yscroll = Scrollbar(self.frame)
        self.yscroll.pack(side="right", fill="y")
        
        self.canvas = Canvas(self.frame, yscrollcommand=self.yscroll.set, width=w, height=h)
        self.canvas.pack(side="left", fill="both", expand=FALSE)
        self.yscroll.config(command=self.canvas.yview)

        self.f = Frame(self.frame)
        self.f.pack(expand=FALSE)
        self.canvas.create_window(0, 0, window=self.f, anchor='nw')

    def update(self):
        self.frame.update()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        