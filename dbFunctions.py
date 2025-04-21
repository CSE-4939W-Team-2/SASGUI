import sqlite3
import json
import time

db_location = 'database\SDPDatabase.sqlite'
user_table = 'users'
scans_table = 'scans'

'Adds row to given table'
def add_to_table(db_location, table_name, new_values):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    placeholders = ", ".join(["?"] * len(new_values))
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.execute(query, new_values)
    conn.commit()
    conn.close()

'Deletes row from given table based on condition'
def delete_row(db_location, table_name, column_name, value):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {column_name} = ?"
    cursor.execute(query, (value,))
    conn.commit()
    conn.close()

'Queries table and returns matching rows'
def query_table(db_location, table_name, column_name=None, value=None):
    conn = sqlite3.connect(db_location)
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
    add_to_table(db_location, user_table, (user_id))
    
'Adds a scan along with parameters to the scans table'
def add_to_scans(file_name, file_data, parameter_dict, user_id = 1):
    # Validate the scan data before adding it
    if not validate_scan_file(file_data):
        print("Error: This is not a valid scan graph file. Scattering data is out of bounds or cannot be plugged in.")
        return
    
    parameters_json = json.dumps(parameter_dict)
    new_values = (user_id, file_name, file_data, parameters_json)
    add_to_table(db_location, user_table, new_values)

'Retrieves all scans for a specific user_id'
def get_user_scans(user_id):
    return query_table(db_location, "scans", "UserID", user_id)

'Retrieves all scans that match the curve_type'
def get_scans_by_curve(curve_type):
    return query_table(db_location, "scans", "CurveType", curve_type)

'Retrieves the scan parameters and converts into a dictionary'
def get_scan_parameters(scan_id):
    result = query_table(db_location, "scans", "ScanID", scan_id)
    if result:
        return json.loads(result[0][-1])  # Last column contains JSON
    return None

'Validates the scan file data'
def validate_scan_file(file_data):
    # Example validation logic - you should replace this with your actual validation rules
    # For this example, we'll assume file_data is a list of numbers
    try:
        scattering_data = json.loads(file_data)
        min_bound = 0  # Example lower bound for scattering data
        max_bound = 100  # Example upper bound for scattering data

        # Check if scattering data is within bounds
        for value in scattering_data:
            if value < min_bound or value > max_bound:
                return False

        # If everything is within bounds
        return True
    except (json.JSONDecodeError, TypeError):
        # If the file_data is not a valid JSON or type mismatch
        return False

if __name__ == "__main__":
    add_to_users((123123123,))