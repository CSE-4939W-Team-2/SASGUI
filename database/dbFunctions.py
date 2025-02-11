import sqlite3 
import json

db_name = 'SDPDatabase.sqlite'
user_table = 'users'
scans_table = 'scans'

'Adds row to given table'
def add_to_table(db_name, table_name, new_values):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    placeholders = ", ".join(["?"] * len(new_values))
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.execute(query, new_values)
    conn.commit()
    conn.close()

'Deletes row from given table based on condition'
def delete_row(db_name, table_name, column_name, value):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {column_name} = ?"
    cursor.execute(query, (value,))
    conn.commit()
    conn.close()

'Queries table and returns matching rows'
def query_table(db_name, table_name, condition='1=1'):
    '1=1 is the default which checks all rows'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name} WHERE {condition}')
    results = cursor.fetchall()
    conn.close()
    return results

'Adds a user to the users table'
def add_to_users(user_id):
    add_to_table(db_name, user_table, (user_id))
    
'Adds a scan along with parameters to the scans table'
def add_to_scans(user_id, file_path, curve_type, parameter_dict):
    parameters_json = json.dumps(parameter_dict)
    new_values = (user_id, file_path, curve_type, parameters_json)
    add_to_table(db_name, user_table, new_values)