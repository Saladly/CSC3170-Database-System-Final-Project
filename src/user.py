from db import fetch_results, execute_query

def login(username, password):
    query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    result = fetch_results(query, (username, password))
    if result:
        return result[0]
    return None

def get_user_role(user_id):
    query = "SELECT role FROM Users WHERE user_id = %s"
    result = fetch_results(query, (user_id,))
    return result[0]['role'] if result else None

def register_user(username, password, role):
    """
    Registers a new user as a Patron or Librarian.
    """
    if role not in ['patron', 'librarian']:
        print("Invalid role. Please choose either 'patron' or 'librarian'.")
        return
    
    # SQL query to insert a new user into the Users table
    query = """
    INSERT INTO Users (username, password, role) 
    VALUES (%s, %s, %s);
    """
    
    # Execute the query to insert the new user
    result = execute_query(query, (username, password, role))
    
    if result:
        print(f"Registration successful! Welcome, {username}!")
    else:
        print("An error occurred during registration.")
