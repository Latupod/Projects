import sqlite3 as sq

connection = sq.connect("NavigationAppData.db")
cursor = connection.cursor()

cursor.execute('''DROP TABLE IF EXISTS test_table1''')

create_query = (''' CREATE TABLE LoginDetails
(               Username Text ,
                Password TEXT, 
                Key TEXT,
                PRIMARY KEY (Username,Password)
                );
                ''')
cursor.execute(create_query)

create_query = (''' CREATE TABLE TimetableMonday
(               Username Text ,
                Day TEXT,
                P1 TEXT, 
                P2 TEXT,
                P3 TEXT, 
                P4 TEXT,
                P5 TEXT, 
                P6 TEXT,
                P7 TEXT, 
                P8 TEXT,
                PRIMARY KEY (Username)
                );
                ''')

create_query = (''' CREATE TABLE TimetableTuesday
                (               
                Username Text ,
                Day TEXT,
                P1 TEXT, 
                P2 TEXT,
                P3 TEXT, 
                P4 TEXT,
                P5 TEXT, 
                P6 TEXT,
                P7 TEXT, 
                P8 TEXT,
                PRIMARY KEY (Username)
                );
                ''')
cursor.execute(create_query)

create_query = (''' CREATE TABLE TimetableWednesday
                (               
                Username Text ,
                Day TEXT,
                P1 TEXT, 
                P2 TEXT,
                P3 TEXT, 
                P4 TEXT,
                P5 TEXT, 
                P6 TEXT,
                P7 TEXT, 
                P8 TEXT,
                PRIMARY KEY (Username)
                );
                ''')
cursor.execute(create_query)

create_query = (''' CREATE TABLE TimetableThursday
                (               
                Username Text ,
                Day TEXT,
                P1 TEXT, 
                P2 TEXT,
                P3 TEXT, 
                P4 TEXT,
                P5 TEXT, 
                P6 TEXT,
                P7 TEXT, 
                P8 TEXT,
                PRIMARY KEY (Username)
                );
                ''')
cursor.execute(create_query)

create_query = (''' CREATE TABLE TimetableFriday
                (               
                Username Text ,
                Day TEXT,
                P1 TEXT, 
                P2 TEXT,
                P3 TEXT, 
                P4 TEXT,
                P5 TEXT, 
                P6 TEXT,
                P7 TEXT, 
                P8 TEXT,
                PRIMARY KEY (Username)
                );
                ''')
cursor.execute(create_query)


#insert_query = (''' INSERT INTO test_table1 VALUES("test1-1","test1-2","test1-3")''')
#cursor.execute(insert_query)

connection.commit()
connection.close()