import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_table():

    c.execute('''
                CREATE TABLE IF NOT EXISTS type
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )              
              
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS storage
              (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER,
                type INTEGER,
                price INTEGER,
                date STAMP,
                FOREIGN KEY(type) REFERENCES type(id)
              )
              ''')
    

    c.execute('''
              CREATE TABLE IF NOT EXISTS wallet
              (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  count INTEGER,
                  type INTEGER,
                  price INTEGER,
                  date STAMP,
                  FOREIGN KEY(type) REFERENCES type(id)
              )            
              ''')
    

    c.execute('''
              
              CREATE TABLE IF NOT EXISTS returns
              (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  count INTEGER,
                  type INTEGER,
                  price INTEGER,
                  date STAMP,
                  FOREIGN KEY(type) REFERENCES type(id)
              )  

              ''')
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS indebtedness
              (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  type TEXT,
                  price INTEGER,
                  date STAMP
              )
              ''')

create_table()
conn.commit()
conn.close()