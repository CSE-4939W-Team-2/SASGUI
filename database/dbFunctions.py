import sqlite3 

dbName = 'SDPDatabase.sqlite'
userTable = 'users'
scansTable = 'scans'

def addToTable(dbName, tableName, newValue):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute(f'insert into {tableName} Values ({newValue})')
    conn.commit()
    conn.close()

    