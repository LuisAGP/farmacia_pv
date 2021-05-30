from tkinter import *
from Vistas.Vista_Caja import Caja
from Vistas.Vista_Inventario import Inventario


class Menu_Bar():
    def __init__(self, root):
        self.root = root
        self.menu_bar = Menu(self.root)
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height() - 25
        self.vista_activa = ""
        self.crear_menu()

        # Iniciamos la vista de caja
        # self.caja()
        self.inventario()
    
    def crear_menu(self):
        self.root.config(menu=self.menu_bar)

        inicmenu = Menu(self.menu_bar, tearoff=0)
        editmenu = Menu(self.menu_bar, tearoff=0)
        helpmenu = Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="Inicio", menu=inicmenu)
        self.menu_bar.add_cascade(label="Editar", menu=editmenu)
        self.menu_bar.add_cascade(label="Ayuda", menu=helpmenu)

        inicmenu.add_command(label="Caja", command=self.caja)
        inicmenu.add_command(label="Inventario", command=self.inventario)
        inicmenu.add_separator()
        inicmenu.add_command(label="Salir", command=self.root.quit)
        

    

    def caja(self):
        if self.vista_activa != "CAJA":
            self.clear()
            self.vista_activa = "CAJA"
            width = self.root.winfo_width()
            height = self.root.winfo_height() - 25
            Caja(self.root, width=width, height=height)

    
    def inventario(self):
        if self.vista_activa != "INVENTARIO":
            self.clear()
            self.vista_activa = "INVENTARIO"
            width = self.root.winfo_width()
            height = self.root.winfo_height() - 25
            Inventario(self.root, width=width, height=height)

    
    def clear(self):
        list = self.root.grid_slaves()
        
        for i in list:
            i.destroy()


