import sqlite3
from sqlite3 import Error
from db_connection import Connection

# Este es el principal archivo del proyecto
def main():
    db = Connection()
    db.create_connection()
    
    registrar_producto(db.conn)

    db.close_connection()


def registrar_producto(coneccion):
    nombre_producto = input("Nombre del producto: ")
    nombre_componente = input("Nombre del componente: ")
    porcion = input("cantidad de porcion: ")
    tipo_porcion = input("medida de porcion: ")
    requiere_reseta = input("¿Requiere receta? ")
    precio = input("Precio: ")
    codigo = input("Codigo de barras: ")


    sql = ''' 
        INSERT INTO productos(nombre_producto, componente, porcion, tipo_porcion, requiere_receta, precio, codigo)
        VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')
    '''.format(nombre_producto, nombre_componente, porcion, tipo_porcion, requiere_reseta, precio, codigo)

    cur = coneccion.cursor()
    cur.execute(sql)
    coneccion.commit()


if __name__ == "__main__":
    main()

