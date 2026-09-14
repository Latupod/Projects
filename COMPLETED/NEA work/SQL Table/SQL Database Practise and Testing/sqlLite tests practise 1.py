import sqlite3
# to connect with hotel_data database
connection = sqlite3.connect('hotel_data.db')
#connection.execute(''' CREATE TABLE hotel
#         (FIND INT PRIMARY KEY     NOT NULL,
#         FNAME           TEXT    NOT NULL,
#         COST            INT     NOT NULL,
#         WEIGHT        INT);
#         ''')
connection.execute("INSERT INTO hotel VALUES (1, 'cakes',800,10 )")
connection.execute("INSERT INTO hotel VALUES (2, 'biscuits',100,20 )")
connection.execute("INSERT INTO hotel VALUES (3, 'chocos',1000,30 )")

print("All data in food table:") 
cursor = connection.execute("SELECT * from hotel ")
for row in cursor:
    print(row)

print("\nFood id and Food Name:")
cursor = connection.execute("SELECT FIND,FNAME from hotel")
for row in cursor:
    print(row)

#conection.commit() #confirms and saves database changes
connection.close()

###
'''
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
'''
####
'''
import sqlite3
try:
    # Connect to DB and create a cursor
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()
    print('DB Init')
    # Write a query and execute it with cursor
    query = 'select sqlite_version();'
    cursor.execute(query)
    # Fetch and output result
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))
    # Close the cursor
    cursor.close()
# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
# Close DB Connection irrespective of success
# or failure
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')
'''