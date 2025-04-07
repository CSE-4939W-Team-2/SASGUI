import sqlite3
import json
import time

db_location = 'database\SDPDatabase.sqlite'
user_table = 'users'
#users table column names in order: userId, username, password, email, securityQuestion, securityAnswer
scans_table = 'scans'
#scans table column names in order: userId, fileName, fileData

'Adds row to given table'
def add_to_table(db_location, table_name, column_names, new_values):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    columns = ", ".join(column_names)
    placeholders = ", ".join(["?"] * len(new_values))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
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

"""Changes an entry in the database based on a condition."""
def change_entry(db_location, table_name, column_name, new_value, condition_column, condition_value):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?"
    cursor.execute(query, (new_value, condition_value))
    conn.commit()
    conn.close()




'Adds a user to the users table'
def add_to_users(username, password, email, securityQuestion = '', securityAnswer = ''): # Securely speaking this should be a hashed password, but this is basically set up to accept any string.
    columns = ["username", "password", "email", 'securityQuestion', 'securityAnswer']
    values = (username, password, email, securityQuestion, securityAnswer)
    add_to_table(db_location, user_table, columns, values)
    
    
'Adds a scan along with parameters to the scans table'
def add_to_scans(file_name, file_data, userId = 1):
    columns = ["userId", "fileName", "fileData"]
    new_values = (userId, file_name, file_data)
    add_to_table(db_location, scans_table, columns, new_values)

'Retrieves all scans for a specific userId'
def get_user_scans(userId):
    return query_table(db_location, "scans", "userId", userId)

"""Retrieves user info for a specific userId."""
def get_user_info(userId):
    result = query_table(db_location, user_table, "userId", userId)
    if result:
        return {
            "userId": result[0][0], #I'm aware this is redundant
            "username": result[0][1],
            "password": result[0][2],
            "email": result[0][3],
            "security_question": result[0][4],
            "security_answer": result[0][5]
        }
    return None

"""Retrieves the user info for a specific username."""
def get_id_by_username(username):
    result = query_table(db_location, user_table, "username", username)
    if result:
        return {
            "userId": result[0][0]
        }
    return None

"""Retrieves the user info for a specific username."""
def get_id_by_email(email):
    result = query_table(db_location, user_table, "email", email)
    if result:
        return {
            "userId": result[0][0]
        }
    return None

'Retrieves all scans that match the curve_type'
def get_scans_by_curve(curve_type):
    return query_table(db_location, "scans", "CurveType", curve_type) #This function will not work now that curve type is held within the large string(of a dictionary) in the fileData column

'Retrieves the scan parameters and converts into a dictionary'
def get_scan_parameters(fileName):
    result = query_table(db_location, "scans", "fileName", fileName)
    if result:
        return json.loads(result[0][-1])  # Last column contains JSON
    return None

"""Changes the password for a specific userId."""
def change_password_by_userId(userId, new_password):
    if not new_password:
        raise ValueError("New password cannot be empty.")
    change_entry(db_location, user_table, "password", new_password, "userId", userId)

if __name__ == "__main__":
    print("Nothing to run here")  # Test to see if the database connection works and retrieves users