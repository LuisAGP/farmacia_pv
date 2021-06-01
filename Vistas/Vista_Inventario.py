from tkinter import *

class Inventario:
    def __init__(self, parent, width=800, height=600):
        parent.title("INVENTARIO")
        
        self.parent = Frame(parent)
        self.parent.grid(row=1, column=1, sticky="news")
        self.parent.columnconfigure(1, weight=1)
        self.parent.rowconfigure(1, weight=1)
        self.parent.grid_propagate(0)

        self.root = Frame(self.parent)
        self.root.grid(row=1, column=1, sticky="news")
        self.root.config(pady=30, padx=50)
        self.root.grid_propagate(0)

        self.root.columnconfigure(1, weight=1)

        self.frame = Frame(self.root, bg="#198CC9", height=40)
        self.frame.grid(row=1, column=1, sticky="news")
        
        self.frame.columnconfigure(1, weight=5)
        self.frame.columnconfigure(2, weight=15)
        self.frame.columnconfigure(3, weight=1)

        Label(self.frame, text="PRODUCTOS", bg="#198CC9", fg="white", anchor="w").grid(row=1, column=1, sticky="news", padx=10, pady=8)

        self.nuevo = Button(self.frame, text="Nuevo", bg="#239B56", fg="white", activebackground="#28B463")
        self.nuevo.grid(row=1, column=3, sticky="news", padx=10, pady=8)


        