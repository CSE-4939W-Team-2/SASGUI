import sqlite3
import json
import time

DB_LOCATION = 'database/SDPDatabase.sqlite'
DB_LOCATION = 'database/SDPDatabase.sqlite'
USER_TABLE = 'users'
#users table column names in order: userId, username, password, email, securityQuestion, securityAnswer
SCANS_TABLE = 'scans'
#scans table column names in order: userId, fileName, fileData

'Adds row to given table'
def add_to_table(table_name, column_names, new_values, db_location = DB_LOCATION):
    try:
        conn = sqlite3.connect(db_location)
        cursor = conn.cursor()
        columns = ", ".join(column_names)
        placeholders = ", ".join(["?"] * len(new_values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, new_values)
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": "Username already taken", "error": f"Integrity error: {str(e)}"}
    finally:
        conn.close()
    return {"success": True, "message": "Row added successfully"}

def add_or_replace_to_table(table_name, column_names, new_values, db_location = DB_LOCATION):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    columns = ", ".join(column_names)
    placeholders = ", ".join(["?"] * len(new_values))
    query = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, new_values)
    conn.commit()
    conn.close()

'Deletes row from given table based on condition'
def delete_row( table_name, column_name, value, db_location = DB_LOCATION):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {column_name} = ?"
    cursor.execute(query, (value,))
    conn.commit()
    conn.close()

'Queries table and returns matching rows'
def query_table(table_name, column_name=None, value=None, db_location = DB_LOCATION):
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
def change_entry( table_name, column_name, new_value, condition_column, condition_value, db_location = DB_LOCATION):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?"
    cursor.execute(query, (new_value, condition_value))
    conn.commit()
    conn.close()




'Adds a user to the users table'
def add_to_users(username, password, email, securityQuestion = "", securityAnswer = ""): # Securely speaking this should be a hashed password, but this is basically set up to accept any string.
    columns = ["username", "password", "email", "securityQuestion", "securityAnswer"]
    values = (username, password, email, securityQuestion, securityAnswer)
    return add_to_table(USER_TABLE, columns, values, DB_LOCATION)
    
	

def add_to_scans(file_name, file_data, userId = 1): 
    # Validate the scan data before adding it
    #Validation here does not work the file data is a string, not numbers
    #if not validate_scan_file(file_data):
    #    print("Error: This is not a valid scan graph file. Scattering data is out of bounds or cannot be plugged in.")
    #    return
    
    new_values = (userId, file_name, file_data)
    columns = ["userId", "fileName", "fileData"] 
    add_or_replace_to_table( SCANS_TABLE, columns, new_values, DB_LOCATION)


'Retrieves all scans for a specific userId'
def get_user_scans(userId):
    return query_table("scans", "userId", userId)

"""Retrieves user info for a specific userId."""
def get_user_info(userId):
    result = query_table(USER_TABLE, "userId", userId, DB_LOCATION)
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
    result = query_table(USER_TABLE, "username", username, DB_LOCATION)
    if result:
        return {
            "userId": result[0][0]
        }
    return None

"""Retrieves the user info for a specific username."""
def get_id_by_email(email):
    result = query_table(USER_TABLE, "email", email, DB_LOCATION)
    if result:
        return {
            "userId": result[0][0]
        }
    return None

'Retrieves all scans that match the curve_type'
def get_scans_by_curve(curve_type):
    return query_table("scans", "CurveType", curve_type, DB_LOCATION) #This function will not work now that curve type is held within the large string(of a dictionary) in the fileData column

'Retrieves the scan parameters and converts into a dictionary'
def get_scan_parameters(fileName):
    result = query_table( "scans", "fileName", fileName, DB_LOCATION)
    if result:
        return json.loads(result[0][-1])  # Last column contains JSON
    return None

"""Changes the password for a specific userId."""
def change_password_by_userId(userId, new_password):
    if not new_password:
        raise ValueError("New password cannot be empty.")
    change_entry(USER_TABLE, "password", new_password, "userId", userId, DB_LOCATION)

# In dbFunctions.py

def get_scan_data_by_name_and_user_id(userId, scan_name):
    """Retrieve scan data based on userId and scan name."""
    try:
        conn = sqlite3.connect(DB_LOCATION)
        cursor = conn.cursor()

        # Query for the specific scan for the given userId and fileName (scan_name)
        query = f"SELECT * FROM {SCANS_TABLE} WHERE userId = ? AND fileName = ?"
        cursor.execute(query, (userId, scan_name))

        result = cursor.fetchall()

        conn.close()

        # If there's a result, return it. Otherwise, return None
        if result:
            return {
                "userId": result[0][0],  # Assuming the first column is userId
                "fileName": result[0][1],  # Assuming the second column is fileName
                "fileData": json.loads(result[0][2])  # Assuming the third column is fileData (JSON)
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving scan data by name and userId: {e}")
        return None
'Validates the scan file data'
def validate_scan_file(file_data):
    # Example validation logic - you should replace this with your actual validation rules
    # For this example, we'll assume file_data is a list of numbers
    try:
        scattering_data = json.loads(file_data)
        min_bound = 0  # Example lower bound for scattering data
        max_bound = 100000  # Example upper bound for scattering data

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
    print("Nothing to run here")  # Test to see if the database connection works and retrieves users
    print(get_user_scans(1))  # This should print the contents of the users table