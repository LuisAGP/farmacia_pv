from tkinter import *


class Menu_Bar():
    def __init__(self, root):
        self.root = root
        self.menu_bar = Menu(self.root)
        self.crear_menu()
    
    def crear_menu(self):
        self.root.config(menu=self.menu_bar)

        inicmenu = Menu(self.menu_bar, tearoff=0)
        editmenu = Menu(self.menu_bar, tearoff=0)
        helpmenu = Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="Inicio", menu=inicmenu)
        self.menu_bar.add_cascade(label="Editar", menu=editmenu)
        self.menu_bar.add_cascade(label="Ayuda", menu=helpmenu)

        inicmenu.add_command(label="Caja")
        inicmenu.add_command(label="Inventario")
        inicmenu.add_separator()
        inicmenu.add_command(label="Salir", command=self.root.quit)


