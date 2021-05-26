from tkinter import * 
from PIL import Image, ImageTk
from DB.db_connection import obtener_productos
from modal.Modal import Confirm, Pay_Modal
from General.Utils import number_format

class Caja():
    def __init__(self, container, width=100, height=100): 
        # Parent Frame
        container.title("CAJA")
        self.parent = container       
        
        # Tamaños de componenetes dinamicos
        w_30_s = width * 0.3 - 25 # version con scroll
        w_70_s = width * 0.7 - 25 # version con scroll
        w_30 = width * 0.3 # sin scroll
        w_70 = width * 0.7 # sin scroll
        h_80 = height * 0.8
        h_75 = height * 0.75
        h_20 = height * 0.2
        h_05 = height * 0.05

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
        self.add_productos_lateral()
        # FIN --------------------------- Barra de productos lateral -------------------------------


        # INICIO --------------------------- Caja -------------------------------
        
        # Encabezados caja ------------------------------------>
        self.tabla_caja = Frame(container, width=w_70, height=h_05)
        self.tabla_caja.grid(row=1, column=2)
        self.tabla_caja.grid_propagate(0)

        self.desc = Label(self.tabla_caja, text="NOMBRE / COMPONENTE", justify=CENTER, bg="#198CC9", fg="white", font=("Helvetica", 12, "bold"), bd=1, relief="solid")
        self.cant = Label(self.tabla_caja, text="CANTIDAD",            justify=CENTER, bg="#198CC9", fg="white", font=("Helvetica", 12, "bold"), bd=1, relief="solid")
        self.preu = Label(self.tabla_caja, text="PRECIO UNITARIO",     justify=CENTER, bg="#198CC9", fg="white", font=("Helvetica", 12, "bold"), bd=1, relief="solid")
        self.tota = Label(self.tabla_caja, text="TOTAL",               justify=CENTER, bg="#198CC9", fg="white", font=("Helvetica", 12, "bold"), bd=1, relief="solid")
        
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

        self.canvas_caja = Canvas(self.main_frame_caja, width=w_70_s, height=h_75)
        self.canvas_caja.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scroll_caja = Scrollbar(self.main_frame_caja, orient=VERTICAL, command=self.canvas_caja.yview)
        self.scroll_caja.pack(side=RIGHT, fill=Y)

        self.canvas_caja.configure(yscrollcommand=self.scroll_caja.set)
        self.canvas_caja.bind("<Configure>", lambda e: self.configure_event(e, self.canvas_caja))

        self.frame_caja = Frame(self.canvas_caja)
        self.frame_caja.bind("<Configure>", lambda e: self.configure_event(e, self.canvas_caja))
        self.frame_caja.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas_caja))
        self.canvas_caja.create_window((0, 0), window=self.frame_caja, anchor="nw", width=w_70_s)

        self.frame_caja.columnconfigure(1, weight=1)

        # Variables usadas en la caja
        self.carrito       = [] # Variable que contendra los prodcutos en el carrito
        self.filas         = [] # lista para almacenar los componentes de cada fila de productos en la caja
        self.btn_menos_mas = [] # Lista para almacenar los botones de control de cada fila
        # FIN --------------------------- Caja -------------------------------
        

        # INICIO --------------------------- Control -------------------------------
        self.control = Frame(container, width=w_30, height=h_20)
        self.control.grid(row=3, column=1)
        self.control.config(bd=1, relief="groove")
        self.control.grid_propagate(False)

        self.pagar_img = PhotoImage(file="Images/pagar.png")
        self.cancel_img = PhotoImage(file="Images/cancelar.png")

        self.pay_button = Button(self.control, image=self.pagar_img, text="Pagar", bg="#ABD7F5", bd=0, cursor='hand2', command=self.pagar_carrito)
        self.pay_button.grid(row=1, column=1)
        self.delete_button = Button(self.control, image=self.cancel_img, text="Eliminar productos", bd=0, border=0, cursor='hand2', command=self.cancelar_compra)
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

        # FIN --------------------------- Total -------------------------------




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
    Función agregar los productos disponibles al panel izquierdo de la caja
    @ahutor Luis GP
    @return {None}
    '''
    def add_productos_lateral(self):
        row = 1
        cont = 0

        self.frame_list = []
        self.images_list = []
        self.productos = obtener_productos() # Consulta de productos a la base de datos

        # Calculamos el espacio maximo para el texto en el label
        self.root_barra.update()
        max_wraplength = (self.get_width(self.root_barra) / 2) - 10
        
        for i in self.productos:
            nombre_producto = f"{i['nombre_producto']} {i['porcion']}{i['tipo_porcion']}"
            precio_producto = number_format(i['precio'])
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
            self.l1 = Label(self.frame_list[-1], text=nombre_producto, bg="#198CC9", fg="white", font=("Arial", 16, "bold"), justify=CENTER, wraplength=max_wraplength, cursor="hand2")
            self.l1.pack(fill=BOTH, expand=TRUE, ipady=3)
            
            # Imagen de producto
            self.images_list.append(ImageTk.PhotoImage(Image.open(nombre_imagen)))
            self.l2 = Label(self.frame_list[-1], image=self.images_list[-1], bg="white", height=210, cursor="hand2")
            self.l2.pack(fill=BOTH, expand=TRUE)

            # Precio de producto
            self.l3 = Label(self.frame_list[-1], text=precio_producto, font=('Calibri Light', 12), bg="#198CC9", fg="white", cursor="hand2")
            self.l3.pack(fill=BOTH, expand=TRUE, ipady=5)

            # Agregamos el evento de la rueda del Mouse a todos los elmentos
            self.add_mousevent(self.frame_list[-1], self.canvas_barra)
            self.add_mousevent(self.l1, self.canvas_barra)
            self.add_mousevent(self.l2, self.canvas_barra)
            self.add_mousevent(self.l3, self.canvas_barra)

            # Agregar evento al hacer click a un producto de la barra lateral
            self.l1.bind("<Button-1>", lambda e, producto=i: self.agregar_a_caja(e, producto))
            self.l2.bind("<Button-1>", lambda e, producto=i: self.agregar_a_caja(e, producto))
            self.l3.bind("<Button-1>", lambda e, producto=i: self.agregar_a_caja(e, producto))

            cont += 1





    '''
    Método para agregar o incrementar un producto al carrito
    @author Luis GP
    @param {Event} evento de click
    @param {Dict} Diccionario SQLite del producto
    '''
    def agregar_a_caja(self, event, producto):
        # Convertimos el objeto SQLite a diccionario
        product_dict = dict(zip(producto.keys(), producto[0:]))
        is_in_list = False

        # Comprobamos si el producto seleccionado ya forma parte del carrito
        for item in self.carrito:
            if item['id_producto'] == product_dict['id_producto']:
                is_in_list = self.carrito.index(item)
        
        if is_in_list is not False:
            # incrementamos la cantidad
            self.carrito[is_in_list]['cantidad'] += 1
            
            nueva_cantidad = self.carrito[is_in_list]['cantidad']
            nuevo_total = float(self.carrito[is_in_list]['precio']) * float(nueva_cantidad)

            self.carrito[is_in_list]['total'] = nuevo_total
            
            nuevo_total = number_format(nuevo_total)
            
            self.filas[is_in_list]['total'].set(nuevo_total)
            self.filas[is_in_list]['cantidad'].set(nueva_cantidad)
            
        else:
            # lo agregamos a la lista e incrementamos la cantidad a 1
            self.carrito.append(product_dict)
            self.carrito[-1]['cantidad'] = 1

            # ------------- Colocamos los productos en el carrito -------------------
            nombre   = StringVar()
            precio   = StringVar()
            cantidad = StringVar()
            total    = StringVar()

            nombre.set(f"{self.carrito[-1]['nombre_producto']}\n{self.carrito[-1]['componente']}")
            precio.set(number_format(self.carrito[-1]['precio']))
            cantidad.set("1")
            total.set(number_format(self.carrito[-1]['precio']))

            # Calculamos el espacio maximo para el texto en el label
            self.root_caja.update()
            width_column = self.get_width(self.root_caja) / 6
            w_2 = int(width_column * 2 - 10)
            w_1 = int(width_column)
            h = 60
            
            # Diccionario que conforma una fila en el carrito
            fila = {
                'frow'       : Frame(self.frame_caja, height=h, bg="#5F5F5F"),
                'id_producto': self.carrito[-1]['id_producto'],
                'nombre'     : nombre,
                'precio'     : precio,
                'cantidad'   : cantidad,
                'total'      : total
            }

            # Agregamos el frame a la lista de filas
            self.filas.append(fila)

            r = len(self.carrito) # Fila

            self.filas[-1]['frow'].grid(row=r, column=1, sticky="NSEW", ipady=1)
            self.filas[-1]['frow'].grid_propagate(0)
            self.filas[-1]['frow'].columnconfigure(1, weight=1)
            self.filas[-1]['frow'].columnconfigure(2, weight=2)
            self.filas[-1]['frow'].columnconfigure(3, weight=1)
            self.filas[-1]['frow'].columnconfigure(4, weight=1)


            # Columna 1
            c1 = Frame(self.filas[-1]['frow'], width=w_2)
            c1.grid(row=1, column=1, pady=0, padx=0, sticky="NSEW")
            c1.grid_propagate(0)
            c1.columnconfigure(1, weight=1)
            c1.rowconfigure(1, weight=1)

            desc = Label(c1, textvariable=nombre,   justify=LEFT,   bg="#D6DFF5", fg="#A6A6A6", font=("Helvetica", 9, "bold"), anchor="w", wraplength=w_2)
            desc.grid(row=1, column=1, ipady=1, sticky="NSEW")

            


            # Columna 2
            c2 = Frame(self.filas[-1]['frow'], width=w_2, bg="#D6DFF5")
            c2.grid(row=1, column=2, pady=0, padx=0, sticky="NSEW")
            c2.grid_propagate(0)
            c2.columnconfigure(1, weight=1)
            c2.columnconfigure(2, weight=1)
            c2.columnconfigure(3, weight=1)
            c2.rowconfigure(1, weight=1)
            
            self.btn_menos_mas.append(PhotoImage(file='Images/signo-menos.png'))
            b1 = Button(c2, image=self.btn_menos_mas[-1], bd=0, bg="#D6DFF5", activebackground="#D6DFF5", cursor="hand2", command= lambda e=event, p=producto, r=self.filas[-1]['frow']: self.quitar_de_caja(e, p, r))
            b1.grid(row=1, column=1, padx=(20, 0))
            
            cant = Label(c2, textvariable=cantidad, justify=CENTER, bg="#D6DFF5", fg="#A6A6A6", font=("Helvetica", 9, "bold"))
            cant.grid(row=1, column=2, pady=0, sticky="NSEW")
            
            self.btn_menos_mas.append(PhotoImage(file='Images/signo-de-mas.png'))
            b2 = Button(c2, image=self.btn_menos_mas[-1], bd=0, bg="#D6DFF5", activebackground="#D6DFF5", cursor="hand2", command=lambda e=event, p=producto: self.agregar_a_caja(e, p))
            b2.grid(row=1, column=3, padx=(0, 5))



            # Columna 3
            c3 = Frame(self.filas[-1]['frow'], width=w_1)
            c3.grid(row=1, column=3, pady=0, padx=0, sticky="NSEW")
            c3.grid_propagate(0)
            c3.columnconfigure(1, weight=1)
            c3.rowconfigure(1, weight=1)

            prec = Label(c3, textvariable=precio,   justify=CENTER, bg="#D6DFF5", fg="#A6A6A6", font=("Helvetica", 9, "bold"))
            prec.grid(row=1, column=1, pady=0, sticky="NSEW")




            # Columna 4
            c4 = Frame(self.filas[-1]['frow'], width=w_1, height=h)
            c4.grid(row=1, column=4, pady=0, padx=0, sticky="NSEW")
            c4.grid_propagate(0)
            c4.columnconfigure(1, weight=1)
            c4.rowconfigure(1, weight=1)
            
            tota = Label(c4, textvariable=total,    justify=CENTER, bg="#D6DFF5", fg="#7CBE7E", font=("Helvetica", 9, "bold"))
            tota.grid(row=1, column=1, pady=0, sticky="NSEW")

        self.change_total(self.carrito)

    

    

    '''
    Método para disminuir la cantidad de producto en el carrito
    @author Luis GP
    @param1 {Event}
    @param2 {SQLite Object} producto seleccionado
    @param3 {List} lista de widgets que conforman la fila en el carrito
    @return {None}
    '''
    def quitar_de_caja(self, event, producto, fila):
        # Convertimos el objeto SQLite a diccionario
        product_dict = dict(zip(producto.keys(), producto[0:]))
        index = False

        # Buscamos la pocision del producto en el carrito
        for item in self.carrito:
            if item['id_producto'] == product_dict['id_producto']:
                index = self.carrito.index(item)
        
        if index is not False:
            # incrementamos la cantidad
            self.carrito[index]['cantidad'] -= 1
            
            nueva_cantidad = self.carrito[index]['cantidad']
            nuevo_total = float(self.carrito[index]['precio']) * float(nueva_cantidad)

            self.carrito[index]['total'] = nuevo_total
            
            nuevo_total = number_format(nuevo_total)
            
            self.filas[index]['total'].set(nuevo_total)
            self.filas[index]['cantidad'].set(nueva_cantidad)

            self.change_total(self.carrito)

            if int(self.carrito[index]['cantidad']) <= 0:
                self.carrito.pop(index)
                self.filas.pop(index)
                fila.destroy()
                self.reorganizar_carrito()





    '''
    Método para reacomodar las filas del carrito
    @author Luis GP
    @return {None}
    '''    
    def reorganizar_carrito(self):
        fila = 1
        for item in self.filas:
            item['frow'].grid(row=fila, column=1, sticky="NSEW", ipady=1)
            fila += 1





    '''
    Función para mostar el total $ de los productos en caja
    @ahutor Luis GP
    @params {String} Nueva cantidad calculada
    @return {Float}
    '''
    def change_total(self, carrito=[]):
        total = 0

        if not carrito:
            total = 0
        else:
            for item in carrito:
                total += float(item['cantidad']) * float(item['precio'])
        
        total = number_format(total)
        self.entry_total.config(state=NORMAL)
        self.entry_total.delete(0, 'end')
        self.entry_total.insert(0, total)
        self.entry_total.config(state="readonly")




    '''
    Función para limpiar el carrito
    @author Luis GP
    @return {None}
    '''
    def cancelar_compra(self, confirm=False):
        if confirm:
            for item in self.filas:
                item['frow'].destroy()
            
            self.carrito = []
            self.filas   = []
            self.change_total()
        elif len(self.carrito) > 0:
            msg = "¿Estas seguro que quieres eliminar el carrito?"
            Confirm(self.parent, msg=msg, funcionOk=lambda param=True: self.cancelar_compra(param))
    



    '''
    Método que muestra un modal para realizar el cobro de los productos
    @author Luis GP
    @
    '''
    def pagar_carrito(self):
        if self.entry_total.get() != "$ 0.00":
            total = self.entry_total.get()
            Pay_Modal(self.parent, total, self.carrito, lambda confirm=True: self.cancelar_compra(confirm))
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
