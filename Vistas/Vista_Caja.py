from tkinter import *

class Caja():
    def __init__(self, container, width=100, height=100):

        # Tamaños de componenetes dinamicos
        w_30_s = width * 0.3 - 25 # version con scroll
        w_70_s = width * 0.7 - 25 # version con scroll
        w_30 = width * 0.3 # sin scroll
        w_70 = width * 0.7 # sin scroll
        h_80 = height * 0.8
        h_20 = height * 0.2

        # INICIO --------------------------- Barra de productos lateral -------------------------------
        self.root_barra = Frame(container)
        self.root_barra.grid(row=1, column=1)
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
        # FIN --------------------------- Barra de productos lateral -------------------------------


        # INICIO --------------------------- Caja -------------------------------
        self.root_caja = Frame(container)
        self.root_caja.grid(row=1, column=2)
        self.root_caja.config(bd=3, relief="groove")

        self.main_frame_caja = Frame(self.root_caja)
        self.main_frame_caja.pack(fill=BOTH, expand=TRUE)

        self.canvas_caja = Canvas(self.main_frame_caja, width=w_70_s, height=h_80)
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
        self.control.grid(row=2, column=1)
        self.control.config(bd=3, relief="groove")
        self.control.grid_propagate(False)

        self.pagar_img = PhotoImage(file="Images/pagar.png")
        self.cancel_img = PhotoImage(file="Images/cancelar.png")

        self.pay_button = Button(self.control, image=self.pagar_img, text="Pagar")
        self.pay_button.grid(row=1, column=1)
        self.delete_button = Button(self.control, image=self.cancel_img, text="Eliminar productos")
        self.delete_button.grid(row=2, column=1)
        # FIN --------------------------- Control -------------------------------


        # INICIO --------------------------- Total -------------------------------
        self.total = Frame(container, width=w_70, height=h_20)
        self.total.grid(row=2, column=2)
        self.total.config(bd=3, relief="groove")
        self.total.grid_propagate(False)
    
        self.label = Label(self.total, text="TOTAL: ", font=("Arial", 16, "bold"), pady=40)
        self.label.grid(row=1, column=1)
        self.entry_total = Entry(self.total, justify=CENTER, state="readonly", font=("Helvetica", 14))
        self.entry_total.grid(row=1, column=2)

        self.change_total("$ 1,120.00")
        # FIN --------------------------- Total -------------------------------






    def configure_event(self, event, canvas):
        return canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def add_mousevent(self, component, canvas="b"):
        if canvas.lower() == "b":
            component.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas_barra))
        elif canvas.lower() == "c":
            component.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas_caja))

    def get_width_barra(self):
        return self.canvas_barra.winfo_reqwidth()
    
    def get_height_barra(self):
        return self.canvas_barra.winfo_reqheight()
    
    def get_width_caja(self):
        return self.canvas_caja.winfo_reqwidth()

    def get_height_caja(self):
        return self.canvas_caja.winfo_reqheight()

    def change_total(self, txt):
        self.entry_total.config(state=NORMAL)
        self.entry_total.insert(0, txt)
        self.entry_total.config(state="readonly")

    def destroy(self):
        self.root_barra.destroy()
    

        