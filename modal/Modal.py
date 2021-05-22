from tkinter import *
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


class Pay_Modal:
    def __init__(self, parent, total):
        self.top = Toplevel(parent)
        self.total = self.conver_number(total)
        width = 350
        height = 400

        coor = centrar_modal(width, height, parent)

        self.top.transient(parent)
        self.top.grab_set()
        self.top.geometry(f"{width}x{height}+{coor['x']}+{coor['y']}")
        self.top.title("Pagar compra")
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_propagate(0)

        Label(self.top, text=f"Total de la compra: {total}", font=('Helvetica', 10, 'bold')).grid(row=1, column=1, columnspan=2, sticky='nwes', pady=15)
        
        Label(self.top, text="Efectivo:", justify=LEFT, anchor='w').grid(row=2, column=1, sticky='nwes', padx=(20, 0))

        self.efectivo = Entry(self.top)
        self.efectivo.grid(row=2, column=2, sticky='nwes', padx=(0, 20))


    
    def conver_number(self, cantidad):
        pattern = re.compile(r"[0-9]+?(\.[0-9]+)")
        total = pattern.search(cantidad).group()
        return total




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

