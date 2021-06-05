import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import connect

'''
Clase principal de coneccion a la base de datos
@author Luis GP
'''
class Connection():
    def __init__(self):
        self.db_url = "./DB/pyDB.db"
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
def obtener_productos():
    db = Connection()
    db.create_connection()
    connect = db.conn

    cur = connect.cursor()
    cur.execute("SELECT * FROM productos")

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



