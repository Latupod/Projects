import sqlite3 as sq
import encrypter

def register(username,password):
    connection = sq.connect("NavigationAppData.db")
    cursor = connection.cursor()
    key = encrypter.generate_key()
    encrypted_password = encrypter.encrypt(password,key)
    addtodatabase = [username,encrypted_password,key]
    cursor.executemany(''' INSERT INTO LoginDetails VALUES(?,?,?)''',addtodatabase)
    
    connection.commit()
    connection.close()
