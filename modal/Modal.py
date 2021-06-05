from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from General.Custom_Widgets import Number_Entry
from DB.db_connection import crear_ticket, guardar_producto
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
    def __init__(self, parent, title, msg, width=350, height=120, focus=None, funcion=None):
        self.funcion = funcion
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
        if self.funcion:
            self.funcion()
        if self.focus:
            self.focus.grab_set()






class Pay_Modal:
    def __init__(self, parent, total, carrito, funcion=None):
        self.funcion = funcion
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
        self.efectivo.bind('<Return>', self.pagar)

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




    
    def pagar(self, event=None):
        total = float(self.total)
        
        if self.efectivo.get(): 
            efectivo = float(self.efectivo.get()) 
        else: 
            Alert(self.parent, "::: ¡ALERTA! :::", "El campo efectivo no debe ir vacío", self.width, self.height, self.top)
            return None
        

        if efectivo >= total:
            cambio = number_format(efectivo - total)
            
            crear_ticket(self.carrito, efectivo, cambio)
            self.top.destroy()
            self.funcion()
            Alert(self.parent, "::: ¡ALERTA! :::", f"Cambio: {cambio}", self.width, self.height)
        else:
            Alert(self.parent, "::: ¡ALERTA! :::", "El efectivo es insuficiente", self.width, self.height, self.top)
    



class Nuevo_Producto:
    def __init__(self, parent, funcion=None):
        self.funcion = funcion
        self.parent = parent

        self.top = Toplevel(parent)
        self.width = 400
        self.height = 550

        coor = centrar_modal(self.width, self.height, parent)
        
        self.top.transient(parent)
        self.top.grab_set()
        self.top.geometry(f"{self.width}x{self.height}+{coor['x']}+{coor['y']}")
        self.top.title("Guardar Producto")
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_propagate(0)

        # I-------------------------------------------->Labels<--------------------------------------------

        Label(self.top, text="Nombre del producto:", anchor=E).grid(row=1, column=1, sticky="news")
        Label(self.top, text="Componente:"         , anchor=E).grid(row=2, column=1, sticky="news")
        Label(self.top, text="Porcion:"            , anchor=E).grid(row=3, column=1, sticky="news")
        Label(self.top, text="Tipo de porcion:"    , anchor=E).grid(row=4, column=1, sticky="news")
        Label(self.top, text="Inventario:"         , anchor=E).grid(row=5, column=1, sticky="news")
        Label(self.top, text="Imagen:"             , anchor=E).grid(row=6, column=1, sticky="news")
        Label(self.top, text="Codigo:"             , anchor=E).grid(row=7, column=1, sticky="news")
        Label(self.top, text="Precio:"             , anchor=E).grid(row=8, column=1, sticky="news")

        # F-------------------------------------------->Labels<--------------------------------------------



        # I------------------------------------->Nombre del producto<--------------------------------------

        self.input_name = Entry(self.top)
        self.input_name.grid(row=1, column=2, sticky="news", padx=(10, 20), pady=15)

        # F------------------------------------->Nombre del producto<--------------------------------------



        # I------------------------------------------>Componente<------------------------------------------

        self.input_comp = Entry(self.top)
        self.input_comp.grid(row=2, column=2, sticky="news", padx=(10, 20), pady=15)

        # F------------------------------------------>Componente<------------------------------------------



        # I-------------------------------------------->Porción<-------------------------------------------

        self.input_porcion = Number_Entry(self.top)
        self.input_porcion.grid(row=3, column=2, sticky="news", padx=(10, 20), pady=15)

        # F-------------------------------------------->Porción<-------------------------------------------


        
        # I----------------------------------------->Tipo porción<-----------------------------------------

        self.input_tipo_porcion = ttk.Combobox(self.top, state="readonly")
        self.input_tipo_porcion['values'] = ('g', 'mg', 'kg', 'ml', 'l', 'pz', 'oz')
        self.input_tipo_porcion.current(1)
        self.input_tipo_porcion.grid(row=4, column=2, sticky="news", padx=(10, 20), pady=15)

        # F----------------------------------------->Tipo porción<-----------------------------------------



        # I------------------------------------------>Inventario<------------------------------------------

        self.input_inventario = Number_Entry(self.top)
        self.input_inventario.grid(row=5, column=2, sticky="news", padx=(10, 20), pady=15)

        # F------------------------------------------>Inventario<------------------------------------------



        # I-------------------------------------------->Imagen<--------------------------------------------

        self.frame_img = Frame(self.top)
        self.frame_img.grid(row=6, column=2, sticky="news", padx=(10, 20), pady=15)
        self.frame_img.columnconfigure(1, weight=1)
        self.entry_img = Entry(self.frame_img, state="readonly")
        self.entry_img.grid(row=1, column=1, sticky="news", pady=(5, 0))
        Button(self.frame_img, text="Seleccionar imagen...", cursor="hand2", command=self.open_file).grid(row=2, column=1, sticky="news", pady=(0, 5))
        self.url = ""

        # F-------------------------------------------->Imagen<--------------------------------------------
        


        # I-------------------------------------------->Codigo<--------------------------------------------

        self.input_codigo = Entry(self.top)
        self.input_codigo.grid(row=7, column=2, sticky="news", padx=(10, 20), pady=15)

        # F-------------------------------------------->Imagen<--------------------------------------------

        

        # I-------------------------------------------->Precio<--------------------------------------------

        self.input_precio = Number_Entry(self.top)
        self.input_precio.grid(row=8, column=2, sticky="news", padx=(10, 20), pady=15)

        # F-------------------------------------------->Precio<--------------------------------------------



        # I--------------------------------------->Requiere receta<----------------------------------------
        
        self.requiere_receta = IntVar()
        ttk.Checkbutton(self.top, text="Requiere receta", variable=self.requiere_receta, onvalue=1, offvalue=0).grid(row=9, column=1, columnspan=2, padx=(10, 20), pady=15)

        # F--------------------------------------->Requiere receta<----------------------------------------


        Button(self.top, text="Cancelar", width=8, command=self.cancelar).grid(row=10, column=1, pady=(20, 0))
        Button(self.top, text="Guardar",  width=8, command=self.guardar ).grid(row=10, column=2, pady=(20, 0))
    



    '''
    Función para abrir buscador de archivos
    @author Luis GP
    @return {None}
    '''
    def open_file(self):
        filetypes = (
            ('imagen', '*.png *.jpg *.jpge *.gif'),
        )

        searcher = fd.askopenfilename(filetypes=filetypes)

        self.url = searcher

        self.entry_img.config(state="normal")
        self.entry_img.delete(0, END)
        self.entry_img.insert(0, self.url.split("/")[-1])
        self.entry_img.config(state="readonly")






    def cancelar(self):
        self.top.destroy()


    

    def guardar(self):

        if self.url:
            nombre = self.entry_img.get()
            self.escalar_imagen(self.url, nombre)
        else:
            nombre = "default.jpg"
        
        data = {
            'nombre_producto': self.input_name.get(),
            'componente': self.input_comp.get(),
            'porcion': self.input_porcion.get(),
            'tipo_porcion': self.input_tipo_porcion.get(),
            'inventario': self.input_inventario.get(),
            'imagen': nombre,
            'codigo': self.input_codigo.get(),
            'precio': self.input_precio.get(),
            'requiere_receta': self.requiere_receta.get()
        }

        guardar_producto(data)

        self.top.destroy()
        if self.funcion:
            self.funcion()
        Alert(self.parent, "::: ¡ALERTA! :::", f"¡El producto se guardo correctamente!", 250, 200)

    

    def escalar_imagen(self, url, nombre):
        image = Image.open(url)
        width, height = image.size
        max_size = 200

        if height > width:
            width = int(max_size * width / height)
            height = max_size
        else:
            height = int(max_size * height / width)
            width = max_size

        image = image.resize((width, height))
        image.save(f"Images/Productos/{nombre}")




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
    x = int(( parent.winfo_width()  ) / 2 - m_w / 2)
    y = int(( parent.winfo_height() ) / 2 - m_h / 2)

    return {'x':x, 'y':y}

