from tkinter import * 
from DB.db_connection import obtener_productos
from General.Utils import number_format

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

        self.nuevo = Button(self.frame, text="Nuevo", bg="#239B56", fg="white", activebackground="#28B463")
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

        self.c1 = Label(self.header, text="Acción",     justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
        self.c1.grid(row=1, column=1, sticky="news", padx=(2, 1), pady=1)

        self.c2 = Label(self.header, text="Nombre",     justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
        self.c2.grid(row=1, column=2, sticky="news", padx=1     , pady=1)

        self.c3 = Label(self.header, text="Porción",    justify=CENTER, font=('Arial', 11, ''), bg="#4D4D4D", fg="white", height=30)
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
    Metodo para agregar evento <MouseWheel> para cualquier elemento que este contenido en un frame con scroll
    @author Luis GP
    @params {Tk_object}, {Tk_object}->(Canvas donde se encuentra contenido el panel scrollable) 
    @return {function}
    '''
    def add_mousevent(self, component, canvas):
        component.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, canvas))

    

    def productos_inventario(self):
        
        productos  = obtener_productos()
        self.celda = []
        self.img   = []
        cont = 1

        # Width dinamico para cada columna
        width_c1 = self.c1.winfo_width()
        width_c2 = self.c2.winfo_width()
        width_c3 = self.c3.winfo_width()
        width_c4 = self.c4.winfo_width()
        width_c5 = self.c5.winfo_width()

        for item in productos:

            # Ejemplo
            # Label(self.window, text="Acción", justify=CENTER).grid(row=(int(i) +1), column=1, sticky="news", padx=(2, 1), pady=1)

            # I--------------------------------> Columna Acción <--------------------------------

            # Frame de botones
            self.celda.append(Frame(self.window, width=width_c1, height=30))
            self.celda[-1].grid(row=cont, column=1, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            # Botón para editar
            self.img.append(PhotoImage(file='Images/editar.png'))
            self.boton_editar = Button(self.celda[-1], image=self.img[-1], cursor="hand2")
            self.boton_editar.grid(row=1, column=1)

            # Botón para eliminar
            self.img.append(PhotoImage(file="Images/eliminar.png"))
            self.boton_eliminar = Button(self.celda[-1], image=self.img[-1], cursor="hand2")
            self.boton_eliminar.grid(row=1, column=2)

            # F--------------------------------> Columna Acción <--------------------------------



            # I--------------------------------> Columna Nombre <--------------------------------

            self.celda.append(Frame(self.window, width=width_c2))
            self.celda[-1].grid(row=cont, column=2, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            Label(self.celda[-1], text=f"{item['nombre_producto']}").grid(row=1, column=1, sticky="news", padx=1, pady=1)

            # F--------------------------------> Columna Nombre <--------------------------------



            # I--------------------------------> Columna Porción <-------------------------------

            self.celda.append(Frame(self.window, width=width_c3))
            self.celda[-1].grid(row=cont, column=3, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            Label(self.celda[-1], text=f"{item['porcion']} {item['tipo_porcion']}").grid(row=1, column=1, sticky="news", padx=1, pady=1)

            # F--------------------------------> Columna Porción <-------------------------------



            # I--------------------------------> Columna Precio <--------------------------------

            self.celda.append(Frame(self.window, width=width_c4))
            self.celda[-1].grid(row=cont, column=4, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            precio = number_format(item['precio'])
            Label(self.celda[-1], text=f"{precio}").grid(row=1, column=1, sticky="news", padx=1, pady=1)

            # F--------------------------------> Columna Precio <--------------------------------



            # I------------------------------> Columna Inventario <------------------------------

            self.celda.append(Frame(self.window, width=width_c5))
            self.celda[-1].grid(row=cont, column=5, sticky="ns", padx=(2, 1), pady=1)
            self.celda[-1].columnconfigure(1, weight=1)
            self.celda[-1].rowconfigure(1, weight=1)
            self.celda[-1].grid_propagate(0)

            Label(self.celda[-1], text=f"{item['inventario_actual']}").grid(row=1, column=1, sticky="news", padx=(1, 2), pady=1)

            # I------------------------------> Columna Inventario <------------------------------


            cont += 1