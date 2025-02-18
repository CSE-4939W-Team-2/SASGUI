import sqlite3
import json
import time

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
def query_table(db_name, table_name, column_name=None, value=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if column_name and value:
        query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
        cursor.execute(query, (value,))
    else:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

    results = cursor.fetchall()
    conn.close()
    return results


'Adds a user to the users table'
def add_to_users(user_id):
    add_to_table(db_name, user_table, (user_id))
    
'Adds a scan along with parameters to the scans table'
def add_to_scans(user_id, file_path, curve_type, parameter_dict):
    timestamp = int(time.time())  # Gets current timestamp
    unique_filename = f"{timestamp}_{file_path}"
    parameters_json = json.dumps(parameter_dict)
    new_values = (user_id, unique_filename, curve_type, parameters_json)
    add_to_table(db_name, scans_table, new_values)

'Retrieves all scans for a specific user_id'
def get_user_scans(user_id):
    return query_table(db_name, "scans", "UserID", user_id)

'Retrieves all scans that match the curve_type'
def get_scans_by_curve(curve_type):
    return query_table(db_name, "scans", "CurveType", curve_type)

'Retrieves the scan parameters and converts into a dictionary'
def get_scan_parameters(scan_id):
    result = query_table(db_name, "scans", "ScanID", scan_id)
    if result:
        return json.loads(result[0][-1])  # Last column contains JSON
    return None