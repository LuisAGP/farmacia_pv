from Menu import Menu_Bar
from tkinter import *
import platform

# Este es el principal archivo del proyecto
def main():
    # Configuracion inicial
    root = Tk()

    '''
    ::: NOTA :::
    Este proyecto solo es capaz de visualizarse de manera correcta en pantalla completa
    ::: NOTA :::
    '''
    if platform.system() == "Windows":
        root.state("zoomed")
    elif platform.system() == "Linux":
        root.attributes('-zoomed', True)
    else:
        print("No se pudo ejecutar el programa en tu sistema operativo")
        exit()
        
    root.update()
    root.columnconfigure(0, weight=0)
    root.rowconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)
    root.grid_propagate(0)
    
    # Menu
    Menu_Bar(root)

    root.mainloop()





if __name__ == "__main__":
    main()

