from tkinter import *

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

        # Coordenadas para centrar nuestra ventana
        # Formula:
        #   ( x = Frame_width / 2 )   -  ( modal_widht / 2 )
        #   ( y = Frame_height / 2 )  -  ( modal_height / 2 )
        m_w = 350
        m_h = 120
        x = int(( parent.winfo_reqwidth()  ) / 2 - m_w / 2)
        y = int(( parent.winfo_reqheight() ) / 2 - m_h / 2)

        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.geometry(f"300x100+{x}+{y}")
        self.top.title(title)
        Label(self.top, text=msg, font=("Helvetica", 10), wraplength=(m_w - 50)).pack(fill=BOTH, expand=TRUE, padx=15, pady=5)

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


