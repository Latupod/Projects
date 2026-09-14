import sqlite3 as sq

connection = sq.connect("TestDatabse.db")
cursor = connection.cursor()

# try:
#     cursor.execute('''DROP TABLE test_table1''')
# except sq.Error as error:
#     pass

cursor.execute('''DROP TABLE IF EXISTS test_table1''')

create_query = (''' CREATE TABLE test_table1
(               Key1 INT PRIMARY KEY,
                Var1 TEXT, 
                Var2 TEXT,
                ToUse BOOLEAN);
                ''')
cursor.execute(create_query)

insert_query = (''' INSERT INTO test_table1 VALUES(1,"test1-1","test1-2",False)''')
cursor.execute(insert_query)

toadd = [
    (2,"test2-1","test2-2",False),
    (3,"test3-1","test3-2",False),
    (4,"test4-1","test4-2",False),
]
cursor.executemany(''' INSERT INTO test_table1 VALUES(?,?,?,?)''',toadd)

toprint = cursor.execute(''' SELECT * FROM test_table1;''')

for x in toprint:
    print(x)
print(toprint)


connection.commit()
connection.close()