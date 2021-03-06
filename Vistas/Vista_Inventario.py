from tkinter import * 
from DB.db_connection import obtener_productos, elimnar_prodcutos
from General.Utils import number_format
from modal.Modal import Nuevo_Producto, Confirm, Alert
import os
import sys

class Inventario:
    def __init__(self, parent, width=800, height=600):

       #URL Path 
        if getattr(sys, 'frozen', False):
            application_path = application_path = sys._MEIPASS
        elif __file__:
            application_path = "./"

        self.url = os.path.join(application_path, "")


        parent.title("INVENTARIO")
        self.parent = parent
        
        self.main = Frame(parent)
        self.main.grid(row=1, column=1, sticky="news")
        self.main.columnconfigure(1, weight=1)
        self.main.rowconfigure(1, weight=1)
        self.main.grid_propagate(0)

        self.root = Frame(self.main)
        self.root.grid(row=1, column=1, sticky="news")
        self.root.config(pady=30, padx=50)
        self.root.grid_propagate(0)

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=2)
        self.root.rowconfigure(3, weight=40)


        # I---------------->Etiqueta de panel<------------------------
        self.frame = Frame(self.root, bg="#198CC9")
        self.frame.grid(row=1, column=1, sticky="news")
        
        self.frame.columnconfigure(1, weight=5)
        self.frame.columnconfigure(2, weight=15)
        self.frame.columnconfigure(3, weight=1)

        Label(self.frame, text="PRODUCTOS", bg="#198CC9", fg="white", anchor="w", font=('Helvetica', 12, "bold")).grid(row=1, column=1, sticky="news", padx=10, pady=8)

        self.nuevo = Button(self.frame, text="Nuevo", bg="#239B56", fg="white", activebackground="#28B463", command=self.nuevo)
        self.nuevo.grid(row=1, column=3, sticky="news", padx=10, pady=8)
        # F----------------->Etiqueta de panel<-------------------------


        # I-------------->Encabezados de la tabla<----------------------
        self.header = Frame(self.root, bg="#AEB6BF", height=25)
        self.header.grid(row=2, column=1, sticky="news")
        self.header.grid_propagate(0)
        
        self.header.columnconfigure(1, weight=1)
        self.header.columnconfigure(2, weight=1)
        self.header.columnconfigure(3, weight=1)
        self.header.columnconfigure(4, weight=1)
        self.header.columnconfigure(5, weight=1)
        self.header.rowconfigure(1, weight=1)

        self.c1 = Label(self.header, text="Acci??n",     justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
        self.c1.grid(row=1, column=1, sticky="news", padx=(2, 1), pady=1)

        self.c2 = Label(self.header, text="Nombre",     justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
        self.c2.grid(row=1, column=2, sticky="news", padx=1     , pady=1)

        self.c3 = Label(self.header, text="Porci??n",    justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
        self.c3.grid(row=1, column=3, sticky="news", padx=1     , pady=1)

        self.c4 = Label(self.header, text="Precio",     justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
        self.c4.grid(row=1, column=4, sticky="news", padx=1     , pady=1)

        self.c5 = Label(self.header, text="Inventario", justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
        self.c5.grid(row=1, column=5, sticky="news", padx=(1, 2), pady=1)

        Frame(self.header, bg="#DBDBDB", width=17).grid(row=1, column=6, sticky="news")
        # F-------------->Encabezados de la tabla<----------------------

        self.table = Frame(self.root, bg="#AEB6BF")
        self.table.grid(row=3, column=1, sticky="news")

        self.frame_tabla = Frame(self.table)
        self.frame_tabla.pack(fill=BOTH, expand=TRUE)

        self.canvas = Canvas(self.frame_tabla)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scroll = Scrollbar(self.frame_tabla, orient=VERTICAL, command=self.canvas.yview)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.configure_event(e, self.canvas))

        self.canvas.update()

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height() - 4

        self.window = Frame(self.canvas, bg="#AEB6BF")
        self.window.bind("<Configure>", lambda e: self.configure_event(e, self.canvas))
        self.window.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas))

        self.canvas.create_window((0 , 0), window=self.window, anchor="nw", width=w)

        #self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(4, weight=1)
        self.window.columnconfigure(5, weight=1)
        
        # Llenamos la tabla del inventario
        self.celda = []
        self.productos_inventario()


        




    '''
    Metodo para agregar evento <Configure> para cualquier panel con scroll
    @author Luis GP
    @params {event}, {Tk_Object}
    @return {function}
    '''
    def configure_event(self, event, canvas):
        return canvas.configure(scrollregion=canvas.bbox("all"))



    
    '''
    Evento para que el scroll suba o baje con la ruleta del Mouse
    @author Luis GP
    @params {event}, {Tk_Object}
    @return {function}
    '''
    def on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
        



    '''
    M??todo para agregar evento <MouseWheel> para cualquier elemento que este contenido en un frame con scroll
    @author Luis GP
    @params {Tk_object}, {Tk_object}->(Canvas donde se encuentra contenido el panel scrollable) 
    @return {function}
    '''
    def add_mousevent(self, component, canvas):
        component.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, canvas))

    



    '''
    Funci??n para llenar la tabla de inventario con los datos de los productos en la base de datos
    @author Luis GP
    @return {None}
    '''
    def productos_inventario(self):
        
        productos  = obtener_productos()
        self.img   = []
        cont = 1

        if self.celda:
            for item in self.celda:
                item.destroy()

        # Color de celda
        bg_celda = "#F0F0F0"

        # Width dinamico para cada columna
        width_c1 = self.c1.winfo_width()
        width_c2 = self.c2.winfo_width()
        width_c3 = self.c3.winfo_width()
        width_c4 = self.c4.winfo_width()
        width_c5 = self.c5.winfo_width()

        # Padding botones
        pd = width_c1 * 0.25

        for item in productos:

            # I--------------------------------> Columna Acci??n <--------------------------------

            # Frame de botones
            self.celda.append(Frame(self.window, width=width_c1, height=30, bg=bg_celda))
            self.celda[-1].grid(row=cont, column=1, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=8)
            self.celda[-1].columnconfigure(2, weight=1)
            self.celda[-1].columnconfigure(3, weight=1)
            self.celda[-1].columnconfigure(4, weight=8)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            # Bot??n para editar
            self.img.append(PhotoImage(file=f'{self.url}Images/editar.png'))
            self.boton_editar = Button(
                self.celda[-1], 
                image=self.img[-1], 
                cursor="hand2", 
                bg=bg_celda, 
                activebackground=bg_celda, 
                bd=0, 
                command=lambda id=item['id_producto']: self.editar(id)
            )
            self.boton_editar.grid(row=1, column=2)

            # Bot??n para eliminar 
            self.img.append(PhotoImage(file=f'{self.url}Images/eliminar.png'))
            self.boton_eliminar = Button(
                self.celda[-1], 
                image=self.img[-1], 
                cursor="hand2", 
                bg=bg_celda, 
                activebackground=bg_celda, 
                bd=0,
                command= lambda id=item['id_producto']: self.alerta_eliminar(id)
            )
            self.boton_eliminar.grid(row=1, column=3)

            # F--------------------------------> Columna Acci??n <--------------------------------



            # I--------------------------------> Columna Nombre <--------------------------------

            self.celda.append(Frame(self.window, width=width_c2))
            self.celda[-1].grid(row=cont, column=2, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            Label(self.celda[-1], text=f"{item['nombre_producto']}", bg=bg_celda).grid(row=1, column=1, sticky="news", padx=1, pady=1)

            # F--------------------------------> Columna Nombre <--------------------------------



            # I--------------------------------> Columna Porci??n <-------------------------------

            self.celda.append(Frame(self.window, width=width_c3))
            self.celda[-1].grid(row=cont, column=3, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            Label(self.celda[-1], text=f"{item['porcion']} {item['tipo_porcion']}", bg=bg_celda).grid(row=1, column=1, sticky="news", padx=1, pady=1)

            # F--------------------------------> Columna Porci??n <-------------------------------



            # I--------------------------------> Columna Precio <--------------------------------

            self.celda.append(Frame(self.window, width=width_c4))
            self.celda[-1].grid(row=cont, column=4, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            precio = number_format(item['precio'])
            Label(self.celda[-1], text=f"{precio}", bg=bg_celda).grid(row=1, column=1, sticky="news", padx=1, pady=1)

            # F--------------------------------> Columna Precio <--------------------------------



            # I------------------------------> Columna Inventario <------------------------------

            self.celda.append(Frame(self.window, width=width_c5))
            self.celda[-1].grid(row=cont, column=5, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            Label(self.celda[-1], text=f"{item['inventario_actual']}", bg=bg_celda).grid(row=1, column=1, sticky="news", padx=(1, 2), pady=1)

            # I------------------------------> Columna Inventario <------------------------------


            cont += 1


    

    '''
    Funci??n que muestra el modal para guardar un producto en pantalla
    @author Luis GP
    @return {None}
    '''
    def nuevo(self):
        self.parent.update()
        Nuevo_Producto(self.parent, self.productos_inventario)

    

    def editar(self, id):
        self.parent.update()
        Nuevo_Producto(self.parent, self.productos_inventario, id=id)




    def alerta_eliminar(self, id):
        producto = obtener_productos(id)[0]
        msg = f"??Estas seguro que quieres eliminar '{producto['nombre_producto']} {producto['porcion']}{producto['tipo_porcion']}'?"
        Confirm(self.parent, msg=msg, funcionOk=lambda: self.eliminar_producto(id))

    

    def eliminar_producto(self, id):
        elimnar_prodcutos(id)
        Alert(self.parent, "??Eliminado!", "??El producto fu?? eliminado con exito!", 210, 120, funcion=self.productos_inventario)
