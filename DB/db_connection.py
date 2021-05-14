import sqlite3
from sqlite3 import Error

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