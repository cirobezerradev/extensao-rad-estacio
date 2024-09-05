import psycopg2
from psycopg2 import errors

class ConnectDB:

    def __init__(self) -> None:
        self.conn = self.connect_db()
        self.cursor = self.conn.cursor()

    def connect_db(self):
        return psycopg2.connect(database='dbremessas',
                                user='postgres',
                                host='localhost',
                                password='1234')
    
    def insert_db(self, sql: str, dados: tuple):
        self.cursor.execute(sql, dados)

    def select_db(self, sql: str, dados: tuple) -> tuple:
        self.cursor.execute(sql, dados)
        return self.cursor.fetchall()

    def update_db(self, sql: str, dados: tuple):
        self.cursor.execute(sql, dados)

    def close_db(self) -> None:
        self.cursor.close()
        self.conn.close()

    def create_table(self, sql: str):
        self.cursor.execute(sql)
        self.conn.commit()
