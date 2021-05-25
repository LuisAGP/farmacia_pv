from tkinter import *
from General.Custom_Widgets import Number_Entry
from DB.db_connection import crear_ticket
from General.Utils import number_format
import re

'''
Clase para mostrar el modal de confirmación
@author Luis GP
@param1 {Tk container} Frame, root
@param2 {String} mensaje para mostrar en la alerta por defecto ""
@param2 {String} titulo de la ventana, por defecto "¡ALERTA!
@param3 {function} Función a ejecutar en caso de precionar "Aceptar", por defecto None
@param4 {function} Función a ejecutar en caso de precionar "Cancelar", por defecto None
'''
class Confirm:
    def __init__(self, parent, msg="", title="¡ALERTA!", funcionOk=None, funcionCan=None):
        self.funcionOk = funcionOk
        self.funcionCan = funcionCan

        width = 350
        height = 120

        coor = centrar_modal(width, height, parent)

        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.geometry(f"{width}x{height}+{coor['x']}+{coor['y']}")
        self.top.title(title)
        Label(self.top, text=msg, font=("Helvetica", 10), wraplength=(width - 15)).pack(fill=BOTH, expand=TRUE, padx=15, pady=5)

        self.frame = Frame(self.top)
        self.frame.pack(fill=BOTH, expand=TRUE, anchor=CENTER)

        self.cancel_button = Button(self.frame, text="Cancelar", command=self.cancel)
        self.cancel_button.pack(fill=X, expand=TRUE, side=LEFT, padx=(40, 20))

        self.ok_button = Button(self.frame, text="Aceptar", command=self.ok)
        self.ok_button.pack(fill=X, expand=TRUE, side=RIGHT, padx=(20, 40))


    
    def cancel(self, event=None):
        self.top.destroy()
        if self.funcionCan:
            self.funcionCan()

    

    def ok(self, event=None):
        self.top.destroy()
        if self.funcionOk:
            self.funcionOk()






class Alert:
    def __init__(self, parent, title, msg, width=350, height=120, focus=None):

        self.focus = focus
        coor = centrar_modal(width, height, parent)

        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.geometry(f"{width}x{height}+{coor['x']}+{coor['y']}")
        self.top.title(title)
        Label(self.top, text=msg, font=("Helvetica", 10), wraplength=(width - 15)).pack(fill=BOTH, expand=TRUE, padx=15, pady=5)

        self.aceptar_button = Button(self.top, text="Aceptar", command=self.aceptar, width=10)
        self.aceptar_button.pack(pady=20)

    
    def aceptar(self):
        self.top.destroy()
        if self.focus:
            self.focus.grab_set()






class Pay_Modal:
    def __init__(self, parent, total, carrito):
        self.carrito = carrito
        self.parent = parent
        self.top = Toplevel(parent)
        self.total = self.solo_num(total)
        self.width = 350
        self.height = 200

        coor = centrar_modal(self.width, self.height, parent)

        self.top.transient(parent)
        self.top.grab_set()
        self.top.geometry(f"{self.width}x{self.height}+{coor['x']}+{coor['y']}")
        self.top.title("Pagar compra")
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_propagate(0)

        Label(self.top, text=f"Total de la compra: {total}", font=('Helvetica', 11, 'bold')).grid(row=1, column=1, columnspan=2, sticky='nwes', pady=(20, 50))
        
        Label(self.top, text="Efectivo:", justify=RIGHT, anchor='e').grid(row=2, column=1, sticky='nwes', padx=(20, 0), ipady=3)

        self.efectivo = Number_Entry(self.top)
        self.efectivo.grid(row=2, column=2, sticky='nwes', padx=(0, 20), ipady=3)

        self.cancelar = Button(self.top, text="Cancelar", width=80, command=self.cancelar)
        self.cancelar.grid(row=3, column=1, padx=20, pady=(30, 0))

        self.pagar = Button(self.top, text="Pagar", width=80, command=self.pagar)
        self.pagar.grid(row=3, column=2, padx=20, pady=(30, 0))


    
    def solo_num(self, cantidad):
        pattern = re.compile(r"[0-9]+?(\.[0-9]+)")
        total = pattern.search(cantidad).group()
        return total




    def cancelar(self):
        self.top.destroy()




    
    def pagar(self):
        total = float(self.total)
        
        if self.efectivo.get(): 
            efectivo = float(self.efectivo.get()) 
        else: 
            Alert(self.parent, "::: ¡ALERTA! :::", "El campo efectivo no debe ir vacío", self.width, self.height, self.top)
            return None
        

        if efectivo >= total:
            cambio = number_format(efectivo - total)
            
            crear_ticket(self.carrito, efectivo, cambio)


            Alert(self.parent, "::: ¡ALERTA! :::", f"Cambio: {cambio}", self.width, self.height, self.top)
        else:
            Alert(self.parent, "::: ¡ALERTA! :::", "El efectivo es insuficiente", self.width, self.height, self.top)
    




'''
Función general para colocar los modales al centro del frame padre
@author Luis GP
@param1 {Float} ancho de modal
@param2 {Float} alto de modal
@param3 {Tk_widget} contenedor padre
@return {Dict} coordenadas x, y
'''
def centrar_modal(w, h, parent):
    # Coordenadas para centrar nuestra ventana
    # Formula:
    #   ( x = Frame_width / 2 )   -  ( modal_widht / 2 )
    #   ( y = Frame_height / 2 )  -  ( modal_height / 2 )
    m_w = w
    m_h = h
    x = int(( parent.winfo_reqwidth()  ) / 2 - m_w / 2)
    y = int(( parent.winfo_reqheight() ) / 2 - m_h / 2)

    return {'x':x, 'y':y}

