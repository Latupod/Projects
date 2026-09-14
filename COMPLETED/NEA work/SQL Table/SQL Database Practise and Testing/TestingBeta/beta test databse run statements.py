import sqlite3 as sq

connection = sq.connect("TestDatabse.db")
cursor = connection.cursor()

cursor.execute('''SELECT name FROM sqlite_master WHERE type="table" AND name="test_table1"''')
result = cursor.fetchone()
if result is not None:
    print("Table exists")
else:
    print("Table doesn't exist")

try:
    toprint = cursor.execute(''' SELECT * FROM test_table1;''')

    for x in toprint:
        print(x)
    #print(toprint)
except sq.OperationalError:
    pass

#cursor.execute('''DROP TABLE IF EXISTS test_table1''')
tables = cursor.execute(''' SELECT * FROM sqlite_master WHERE type = "table"''')
print(tables.fetchall())
connection.commit()
connection.close()

