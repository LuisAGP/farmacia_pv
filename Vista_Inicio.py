from tkinter import *

class Inicio():
    def __init__(self, frame):
        self.main_frame = Frame(frame)
        self.main_frame.pack(fill=BOTH, expand=TRUE)

        w = self.get_width() - 25
        h = self.get_height()

        self.canvas = Canvas(self.main_frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        self.scroll = Scrollbar(self.main_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", width=w)

    def get_width(self):
        return self.main_frame.winfo_width()
    
    def get_height(self):
        return self.main_frame.winfo_height()
    

        