import bcrypt
from db import fetch_results, execute_query

# Admin credentials (pre-registered)
ADMIN_USERNAME = "admin"
# Plain text password, will be hashed before storing
ADMIN_PASSWORD = "admin123"  

def login(username, password):
    query = "SELECT * FROM Users WHERE username = %s"
    result = fetch_results(query, (username,))
    if result:
        user = result[0]
        # Compare hashed password
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user
    return None

def get_user_role(user_id):
    query = "SELECT role FROM Users WHERE user_id = %s"
    result = fetch_results(query, (user_id,))
    return result[0]['role'] if result else None

def check_duplicate_username(username):
    query = "SELECT * FROM Users WHERE username = %s"
    result = fetch_results(query, (username,))
    return len(result) > 0

def register_user(username, password, role, admin_user=None):
    # Registers a new user as a Patron or Librarian.
    # Only admin_user can register a librarian.
    if role not in ['patron', 'librarian']:
        print("Invalid role. Please choose either 'patron' or 'librarian'.")
        return
    
    # Check for duplicate username
    if check_duplicate_username(username):
        print("Username is already taken. Please choose a different username.")
        return

    # If role is librarian, only librarian can register a librarian
    if role == 'librarian' and (admin_user is None or admin_user['username'] != ADMIN_USERNAME):
        print("Only the admin can register a librarian.")
        return

    # Hash the password before storing it in the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # SQL query to insert a new user into the Users table
    query = """
    INSERT INTO Users (username, password, role) 
    VALUES (%s, %s, %s);
    """
    
    # Execute the query to insert the new user
    result = execute_query(query, (username, hashed_password.decode('utf-8'), role))
    
    if result:
        print(f"Registration successful! Welcome, {username}!")
    else:
        print("An error occurred during registration.")

def pre_register_admin():
    # Ensures that there is an admin pre-registered in the system.
    if not check_duplicate_username(ADMIN_USERNAME):
        # Hash the admin password before storing it
        hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt())
        query = """
        INSERT INTO Users (username, password, role) 
        VALUES (%s, %s, %s);
        """
        result = execute_query(query, (ADMIN_USERNAME, hashed_password.decode('utf-8'), 'librarian'))
        if result:
            print("Admin account successfully created.")
        else:
            print("An error occurred while creating the admin account.")
