from tkinter import * 

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
        self.header = Frame(self.root, bg="#AEB6BF")
        self.header.grid(row=2, column=1, sticky="news")
        self.header.grid_propagate(0)
        
        self.header.columnconfigure(1, weight=1)
        self.header.columnconfigure(2, weight=1)
        self.header.columnconfigure(3, weight=1)
        self.header.columnconfigure(4, weight=1)
        self.header.columnconfigure(5, weight=1)
        self.header.rowconfigure(1, weight=1)

        Label(self.header, text="Acción",     justify=CENTER).grid(row=1, column=1, sticky="news", padx=(2, 1), pady=1)
        Label(self.header, text="Nombre",     justify=CENTER).grid(row=1, column=2, sticky="news", padx=1     , pady=1)
        Label(self.header, text="Porción",    justify=CENTER).grid(row=1, column=3, sticky="news", padx=1     , pady=1)
        Label(self.header, text="Precio",     justify=CENTER).grid(row=1, column=4, sticky="news", padx=1     , pady=1)
        Label(self.header, text="Inventario", justify=CENTER).grid(row=1, column=5, sticky="news", padx=(1, 2), pady=1)
        Frame(self.header, bg="gray", width=17).grid(row=1, column=6, sticky="news")
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

        self.window = Frame(self.canvas, bg="#AEB6BF", width=w, height=h)
        self.window.bind("<Configure>", lambda e: self.configure_event(e, self.canvas))
        self.window.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas))

        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(4, weight=1)
        self.window.columnconfigure(5, weight=1)
        self.window.grid_propagate(0)
        
        self.canvas.create_window((0 , 0), window=self.window, anchor="nw")
        
        for i in range(100):
            Label(self.window, text="Acción",     justify=CENTER).grid(row=(int(i) +1), column=1, sticky="news", padx=(2, 1), pady=1)
            Label(self.window, text="Nombre",     justify=CENTER).grid(row=(int(i) +1), column=2, sticky="news", padx=1     , pady=1)
            Label(self.window, text="Porción",    justify=CENTER).grid(row=(int(i) +1), column=3, sticky="news", padx=1     , pady=1)
            Label(self.window, text="Precio",     justify=CENTER).grid(row=(int(i) +1), column=4, sticky="news", padx=1     , pady=1)
            Label(self.window, text="Inventario", justify=CENTER).grid(row=(int(i) +1), column=5, sticky="news", padx=(1, 2), pady=1)


        




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