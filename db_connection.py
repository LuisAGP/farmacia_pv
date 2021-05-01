import sqlite3
from sqlite3 import Error

class Connection():
    def __init__(self):
        self.db_url = ".\DB\pyDB.db"
        self.conn = None

    def create_connection(self):

        try:
            self.conn = sqlite3.connect(self.db_url)
        except Error as e:
            print(Error)
            

    def close_connection(self):
        
        if self.conn:
                conn.close()





if __name__ == "__main__":
    Connect = Connection()
    print(Connect.conn)
    Connect.create_connection()
    print(Connect.conn)
