import sqlite3 as sq

def selectlessons():
    connection = sq.connect("NavigationAppData.db")
    cursor = connection.cursor()
    select_query = ('''SELECT * 
                    FROM Timetable 
                    WHERE Username = ''')
    result = cursor.execute(select_query)
    details = []
    for item in result:
        details.append(item)

    connection.close()