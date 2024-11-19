# db.py
import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
import mysql.connector
from assets.config import connect_to_db

# Define basic database functions to execute queries and fetch results.

def execute_query(query, params=None):
    # Executes an SQL query with the provided parameters.

    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

def fetch_results(query, params=None):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results