import sqlite3
from sqlite3 import Error
from db_connection import Connection
from Menu import Menu_Bar
from Vista_Inicio import Inicio
from tkinter import *

# Este es el principal archivo del proyecto
def main():
    # Configuracion inicial
    root = Tk()
    root.wm_state("zoomed")
    root.update()

    # Alto y Ancho de la ventana principal (Pantalla completa)
    width = root.winfo_width()
    height = root.winfo_height() - 25

    # Frame lateral 
    lateral = Frame(root, bg="blue", width=200)
    lateral.grid(row=0, column=0, rowspan=10, columnspan=3)
    lateral.config(bg="lightblue", relief="groove", bd=3, cursor="") 
    caja = Inicio(lateral)


    for i in range(50):
        Button(caja.frame, text=f"Boton {i}").pack(fill=X, expand = True)
    

    # Menu
    menu = Menu_Bar(root)
    #registrar_producto()
    root.mainloop()


# Función para registar un nuevo producto en la farmacia
# @author Luis GP
# @param {SQLite connection object}
# @return void
def registrar_producto():
    db = Connection()
    db.create_connection()
    connect = db.conn

    nombre_producto = input("Nombre del producto: ")
    nombre_componente = input("Nombre del componente: ")
    porcion = input("cantidad de porcion: ")
    tipo_porcion = input("medida de porcion: ")
    requiere_reseta = input("¿Requiere receta? ")
    precio = input("Precio: ")
    codigo = input("Codigo de barras: ")


    sql = f''' 
        INSERT INTO 
        productos(
            nombre_producto, 
            componente, 
            porcion, 
            tipo_porcion, 
            requiere_receta, 
            precio, 
            codigo
        )
        VALUES(
            '{nombre_producto}', 
            '{nombre_componente}', 
            '{porcion}', 
            '{tipo_porcion}', 
            '{requiere_reseta}', 
            '{precio}', 
            '{codigo}'
        )
    '''

    cur = connect.cursor()
    cur.execute(sql)
    connect.commit()

    db.close_connection()


if __name__ == "__main__":
    main()

