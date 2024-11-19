# Used to generate date for database
import random
import bcrypt
from db import execute_query

def load_names():
    # lists of common first and last names.
    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Margaret",
        "Matthew", "Lisa", "Anthony", "Betty", "Donald", "Dorothy", "Mark", "Sandra",
        "Paul", "Ashley", "Steven", "Kimberly", "Andrew", "Donna", "Kenneth", "Emily",
        "George", "Michelle", "Joshua", "Carol", "Kevin", "Amanda", "Brian", "Melissa"
    ]
    # List of 50 Common Last Names
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
        "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
        "Mitchell", "Carter"
    ]
    

    return first_names, last_names

def generate_patrons(num_patrons):
    # Generates and inserts patrons with realistic names into the database.
    first_names = []
    first_names, last_names = load_names()
    usernames = set()
    
    for _ in range(num_patrons):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"{first_name.lower()}.{last_name.lower()}"
        # Ensure uniqueness
        while username in usernames:
            username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 1000)}"
        usernames.add(username)
        
        password = f"pass_{random.randint(1000,9999)}"
        role = 'patron'
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)"
        execute_query(query, (username, hashed_password.decode('utf-8'), role))
    
    print(f"{num_patrons} patrons have been added to the database.")

# Generate 500 patrons
generate_patrons(500)
