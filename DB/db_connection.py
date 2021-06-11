import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import connect
from datetime import datetime
import os
import sys

'''
Clase principal de coneccion a la base de datos
@author Luis GP
'''
class Connection():
    def __init__(self):

        if getattr(sys, 'frozen', False):
            application_path = application_path = sys._MEIPASS
        elif __file__:
            application_path = "./"

        self.db_url = os.path.join(application_path, "DB/pyDB.db")
        self.conn = None

    def create_connection(self):

        try:
            
            self.conn = sqlite3.connect(self.db_url)
            self.conn.row_factory = sqlite3.Row
            
        except Error as e:
            print(e)
            

    def close_connection(self):
        
        if self.conn:
                self.conn.close()





'''
Función para obtener los datos de los productos de la base de datos
@author Luis GP
@return {List}
'''
def obtener_productos(id=None):
    db = Connection()
    db.create_connection()
    connect = db.conn

    where = ""

    if id:
        where = f"AND id_producto = {id} LIMIT 1"

    cur = connect.cursor()
    cur.execute(f"SELECT * FROM productos WHERE deleted_at IS NULL {where}")

    product_list = cur.fetchall()
    db.close_connection()

    return product_list






'''
Función para reflejar una compra en la base de datos
@author Luis GP
@param1 {Dict} diccionario con los productos del carrito
@param2 {Float} pago del cliente
@param3 {Float} cambio del cliente
@return {None}
'''
def crear_ticket(carrito, pago, cambio):
    db = Connection()
    db.create_connection()
    connect = db.conn

    cantidad_productos = 0
    total = 0
    subtotal = 0
    iva = 0
    
    for item in carrito:
        cantidad_productos += int(item['cantidad'])
        total += float(item['cantidad']) * float(item['precio'])
    
    iva = total * 0.16
    subtotal = total - iva

    sql = f''' 
        INSERT INTO 
        ticket(
            cantidad_productos, 
            pago, 
            cambio, 
            total, 
            subtotal, 
            iva
        )
        VALUES(
            '{cantidad_productos}', 
            '{pago}', 
            '{cambio}', 
            '{total}', 
            '{subtotal}', 
            '{iva}'
        )
    '''

    cur = connect.cursor()
    cur.execute(sql)

    id_ticket = cur.lastrowid
    connect.commit()

    for item in carrito:

        total_producto    = float(item['cantidad']) * float(item['precio'])
        iva_producto      = total_producto * 0.16
        subtotal_producto = total_producto - iva_producto

        sql = f''' 
        INSERT INTO 
        detalle_ticket(
            id_ticket, 
            id_producto, 
            cantidad_producto, 
            precio_unitario, 
            total_producto, 
            subtotal_producto,
            iva_producto
        )
        VALUES(
            '{id_ticket}', 
            '{item["id_producto"]}', 
            '{item["cantidad"]}', 
            '{item["precio"]}', 
            '{total_producto}', 
            '{subtotal_producto}',
            '{iva_producto}'
        )
        '''

        cur.execute(sql)
        connect.commit()    


    db.close_connection()





def guardar_producto(data):
    db = Connection()
    db.create_connection()

    connect = db.conn

    if data['id_producto']:
        sql = f'''
        UPDATE productos
            SET nombre_producto = '{data['nombre_producto']}',
                componente = '{data['componente']}',
                porcion = '{data['porcion']}',
                tipo_porcion = '{data['tipo_porcion']}',
                codigo = '{data['codigo']}',
                imagen = '{data['imagen']}',
                inventario_actual = '{data['inventario']}',
                precio = '{data['precio']}',
                requiere_receta = '{data['requiere_receta']}'
            WHERE id_producto = {data['id_producto']}
        '''
    else:
        sql = f'''
        INSERT INTO productos(
            nombre_producto,
            componente,
            porcion,
            tipo_porcion,
            codigo,
            imagen,
            inventario_actual,
            precio,
            requiere_receta
        )
        VALUES(
            '{data['nombre_producto']}',
            '{data['componente']}',
            '{data['porcion']}',
            '{data['tipo_porcion']}',
            '{data['codigo']}',
            '{data['imagen']}',
            '{data['inventario']}',
            '{data['precio']}',
            '{data['requiere_receta']}'
        )
        '''

    cur = connect.cursor()
    cur.execute(sql)

    connect.commit()

    db.close_connection()



def elimnar_prodcutos(id):
    db = Connection()
    db.create_connection()

    connect = db.conn

    now = datetime.now()

    sql = f'''
        UPDATE productos
            SET deleted_at = '{now}'
            WHERE id_producto = {id}
        '''

    cur = connect.cursor()
    cur.execute(sql)

    connect.commit()

    db.close_connection()

