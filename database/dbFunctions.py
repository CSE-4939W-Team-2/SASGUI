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

'Deletes row from given table based on condition'
def deleteRow(dbName, tableName, condition):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {tableName} WHERE {condition}')
    conn.commit()
    conn.close()

'Queries table and returns matching rows'
def queryTable(dbName, tableName, condition='1=1'):
    '1=1 is the default which checks all rows'
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {tableName} WHERE {condition}')
    results = cursor.fetchall()
    conn.close()
    return results