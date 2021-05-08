from tkinter import *

class Inicio():
    def __init__(self, container, width=100, height=100):
        self.root = Frame(container, bg="blue", width=width)
        self.root.pack(side=LEFT)
        self.root.config(bg="lightblue", relief="groove", bd=3, cursor="")
        
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=TRUE)

        self.canvas = Canvas(self.main_frame, width=width, height=height)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        
        self.scroll = Scrollbar(self.main_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.configure_event(e))
        
        self.frame = Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.configure_event(e))
        self.frame.bind("<MouseWheel>", lambda e: self.on_mousewheel(e))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", width=width)

    def configure_event(self, event):
        return self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def add_mousevent(self, component):
        component.bind("<MouseWheel>", lambda e: self.on_mousewheel(e))

    def get_width(self):
        return self.canvas.winfo_reqwidth()
    
    def get_height(self):
        return self.canvas.winfo_reqheight()

    def destroy(self):
        self.root.destroy()
    

        