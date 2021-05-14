from tkinter import * 
from PIL import Image, ImageTk
import sqlite3
from DB.db_connection import Connection

class Caja():
    def __init__(self, container, width=100, height=100):

        # Tamaños de componenetes dinamicos
        w_30_s = width * 0.3 - 25 # version con scroll
        w_70_s = width * 0.7 - 25 # version con scroll
        w_30 = width * 0.3 # sin scroll
        w_70 = width * 0.7 # sin scroll
        h_80 = height * 0.8
        h_77 = height * 0.77
        h_20 = height * 0.2
        h_03 = height * 0.03

        # INICIO --------------------------- Barra de productos lateral -------------------------------
        self.root_barra = Frame(container)
        self.root_barra.grid(row=1, column=1, rowspan=2)
        self.root_barra.config(bg="lightblue", relief="groove", bd=3, cursor="")
        
        self.main_frame_barra = Frame(self.root_barra)
        self.main_frame_barra.pack(fill=BOTH, expand=TRUE)

        self.canvas_barra = Canvas(self.main_frame_barra, width=w_30_s, height=h_80)
        self.canvas_barra.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        self.scroll_barra = Scrollbar(self.main_frame_barra, orient=VERTICAL, command=self.canvas_barra.yview)
        self.scroll_barra.pack(side=RIGHT, fill=Y)

        self.canvas_barra.configure(yscrollcommand=self.scroll_barra.set)
        self.canvas_barra.bind("<Configure>", lambda e: self.configure_event(e, self.canvas_barra))
        
        self.frame_barra = Frame(self.canvas_barra)
        self.frame_barra.bind("<Configure>", lambda e: self.configure_event(e, self.canvas_barra))
        self.frame_barra.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas_barra))
        self.canvas_barra.create_window((0, 0), window=self.frame_barra, anchor="nw", width=w_30_s)
        self.frame_barra.columnconfigure(1, weight=1)
        self.frame_barra.columnconfigure(2, weight=1)
        # FIN --------------------------- Barra de productos lateral -------------------------------


        # INICIO --------------------------- Caja -------------------------------
        
        # Encabezados caja ------------------------------------>
        self.tabla_caja = Frame(container, width=w_70, height=h_03)
        self.tabla_caja.grid(row=1, column=2)
        self.tabla_caja.grid_propagate(0)

        self.desc = Label(self.tabla_caja, text="NOMBRE / COMPONENTE",     justify=CENTER, bg="#878787", fg="white", font=("Candara", 10, "bold"), bd=1, relief="solid")
        self.cant = Label(self.tabla_caja, text="CANTIDAD",        justify=CENTER, bg="#878787", fg="white", font=("Candara", 10, "bold"), bd=1, relief="solid")
        self.preu = Label(self.tabla_caja, text="PRECIO UNITARIO", justify=CENTER, bg="#878787", fg="white", font=("Candara", 10, "bold"), bd=1, relief="solid")
        self.tota = Label(self.tabla_caja, text="TOTAL",           justify=CENTER, bg="#878787", fg="white", font=("Candara", 10, "bold"), bd=1, relief="solid")
        
        self.desc.grid(row=1, column=1, pady=0, sticky="NSEW")
        self.cant.grid(row=1, column=2, pady=0, sticky="NSEW")
        self.preu.grid(row=1, column=3, pady=0, sticky="NSEW")
        self.tota.grid(row=1, column=4, pady=0, sticky="NSEW", padx=(0, 20)) # Padding para compensar el espacio del scroll

        self.tabla_caja.columnconfigure(1, weight=2)
        self.tabla_caja.columnconfigure(2, weight=2)
        self.tabla_caja.columnconfigure(3, weight=1)
        self.tabla_caja.columnconfigure(4, weight=1)

        self.tabla_caja.rowconfigure(1, weight=1)

        # Panel de caja ------------------------------------------>
        self.root_caja = Frame(container)
        self.root_caja.grid(row=2, column=2)
        self.root_caja.config(bd=1, relief="groove")

        self.main_frame_caja = Frame(self.root_caja)
        self.main_frame_caja.pack(fill=BOTH, expand=TRUE)

        self.canvas_caja = Canvas(self.main_frame_caja, width=w_70_s, height=h_77)
        self.canvas_caja.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scroll_caja = Scrollbar(self.main_frame_caja, orient=VERTICAL, command=self.canvas_caja.yview)
        self.scroll_caja.pack(side=RIGHT, fill=Y)

        self.canvas_caja.configure(yscrollcommand=self.scroll_caja.set)
        self.canvas_caja.bind("<Configure>", lambda e: self.configure_event(e, self.canvas_caja))

        self.frame_caja = Frame(self.canvas_caja)
        self.frame_caja.bind("<Configure>", lambda e: self.configure_event(e, self.canvas_caja))
        self.frame_caja.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas_caja))
        self.canvas_caja.create_window((0, 0), window=self.frame_caja, anchor="nw", width=w_70_s)
        # FIN --------------------------- Caja -------------------------------
        

        # INICIO --------------------------- Control -------------------------------
        self.control = Frame(container, width=w_30, height=h_20)
        self.control.grid(row=3, column=1)
        self.control.config(bd=1, relief="groove")
        self.control.grid_propagate(False)

        self.pagar_img = PhotoImage(file="Images/pagar.png")
        self.cancel_img = PhotoImage(file="Images/cancelar.png")

        self.pay_button = Button(self.control, image=self.pagar_img, text="Pagar", bg="#ABD7F5", bd=0, cursor='hand2')
        self.pay_button.grid(row=1, column=1)
        self.delete_button = Button(self.control, image=self.cancel_img, text="Eliminar productos", bd=0, border=0, cursor='hand2')
        self.delete_button.grid(row=1, column=2)

        pdx = int(w_30 / 2) - self.get_width(self.pay_button) - 10
        pdy = int(h_20 / 2) - int(self.get_height(self.pay_button) / 2)
        self.pay_button.grid(padx=(pdx, 10), pady=(pdy, 0))
        self.delete_button.grid(pady=(pdy, 0))
        # FIN --------------------------- Control -------------------------------


        # INICIO --------------------------- Total -------------------------------
        self.total = Frame(container, width=w_70, height=h_20)
        self.total.grid(row=3, column=2)
        self.total.config(bd=1, relief="groove")
        self.total.grid_propagate(False)
        
        self.label = Label(self.total, text="TOTAL: ", font=("Arial", 16, "bold"))
        self.label.grid(row=1, column=1, padx=(50, 0), pady=(40, 0))
        self.entry_total = Entry(self.total, justify=CENTER, state="readonly", font=("Helvetica", 14))
        self.entry_total.grid(row=1, column=2, pady=(40, 0), ipady=2)

        self.change_total("$ 1,120.00")
        # FIN --------------------------- Total -------------------------------

        self.productos = [] # Variable que contendra los productos después de consultar y llenar la barra lateral




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



    '''
    ::: NOTA ::: Solo se uso en pruebas
    Función para obtener el width del panel lateral de la barra
    @author Luis GP
    @return {Float}
    '''
    def get_width_barra(self):
        return self.canvas_barra.winfo_reqwidth()
    


    '''
    ::: NOTA ::: Solo se uso en pruebas
    Función para obtener el height del panel lateral de la barra
    @author Luis GP
    @return {Float}
    '''
    def get_height_barra(self):
        return self.canvas_barra.winfo_reqheight()
    


    '''
    ::: NOTA ::: Solo se uso en pruebas
    Función para obtener el width del panel "frame_caja"
    @author Luis GP
    @return {Float}
    '''
    def get_width_caja(self):
        return self.canvas_caja.winfo_reqwidth()


    '''
    ::: NOTA ::: Solo se uso en pruebas
    Función para obtener el alto del panel "frame_caja"
    @author Luis GP
    @return {Float}
    '''
    def get_height_caja(self):
        return self.canvas_caja.winfo_reqheight()



    '''
    Función para obtener el ancho de cualquier componente
    @ahutor Luis GP
    @params {Tk_object}
    @return {Float}
    '''
    def get_width(self, component):
        return component.winfo_reqwidth()



    '''
    Función para obtener el alto de cualquier componente
    @ahutor Luis GP
    @params {Tk_object}
    @return {Float}
    '''
    def get_height(self, component):
        return component.winfo_reqheight()



    '''
    Función para mostar el total $ de los productos en caja
    @ahutor Luis GP
    @params {String} Nueva cantidad calculada
    @return {Float}
    '''
    def change_total(self, txt):
        self.entry_total.config(state=NORMAL)
        self.entry_total.insert(0, txt)
        self.entry_total.config(state="readonly")


    '''
    Función agregar los productos disponibles al panel izquierdo de la caja
    @ahutor Luis GP
    @params {String} Nueva cantidad calculada
    @return {Float}
    '''
    def add_productos_lateral(self):
        row = 1
        cont = 0

        self.frame_list = []
        self.images_list = []
        self.productos = self.obtener_productos()
        
        for i in self.productos:
            nombre_producto = f"{i['nombre_producto']} {i['porcion']}{i['tipo_porcion']}"
            precio_producto = i['precio']
            nombre_imagen = f'Images/Productos/{i["imagen"]}'

            self.frame_list.append(Frame(self.frame_barra, bd=1, relief="solid"))

            if cont % 2 == 0:
                column=1
                row+=1
            else:
                column=2
            
            self.frame_list[-1].grid(row=row, column=column, sticky="NSEW", padx=5, pady=3)
            self.frame_list[-1].grid_propagate(0)

            # Nombre de producto
            self.l1 = Label(self.frame_list[-1], text=nombre_producto, bg="#198CC9", fg="white", font=("Arial", 16, "bold"), justify=CENTER)
            self.l1.pack(fill=BOTH, expand=TRUE, ipady=3)
            
            # Imagen de producto
            self.images_list.append(ImageTk.PhotoImage(Image.open(nombre_imagen)))
            self.l2 = Label(self.frame_list[-1], image=self.images_list[-1], bg="white", height=210)
            self.l2.pack(fill=BOTH, expand=TRUE)

            # Precio de producto
            self.l3 = Label(self.frame_list[-1], text=precio_producto, font=('Calibri Light', 12), bg="#198CC9", fg="white")
            self.l3.pack(fill=BOTH, expand=TRUE, ipady=5)

            # Agregamos el evento de la rueda del Mouse a todos los elmentos
            self.add_mousevent(self.frame_list[-1], self.canvas_barra)
            self.add_mousevent(self.l1, self.canvas_barra)
            self.add_mousevent(self.l2, self.canvas_barra)
            self.add_mousevent(self.l3, self.canvas_barra)

            # Agregar evento al hacer click izquierdo a un producto de la barra lateral
            self.l2.bind("<Button-1>", lambda e, producto=i: self.agregar_a_caja(e, producto))

            cont += 1



    '''
    Función para obtener los datos de los productos de la base de datos
    @author Luis GP
    @return {List}
    '''
    def obtener_productos(self):
        db = Connection()
        db.create_connection()
        connect = db.conn

        cur = connect.cursor()
        cur.execute("SELECT * FROM productos")

        product_list = cur.fetchall()
        db.close_connection()

        return product_list

    

    def agregar_a_caja(self, event, producto):
        print(producto['nombre_producto'])

'''
Este codigo es para cambiar el tamaño de una imagen
im = Image.open('Images/Productos/Aspirina.jpg')
width, height = im.size
max_size = 200

if height > width:
    width = int(max_size * width / height)
    height = max_size
else:
    height = int(max_size * height / width)
    width = max_size

im = im.resize((width, height))
im.save("Images/Productos/Aspirina-1.jpg")
'''
