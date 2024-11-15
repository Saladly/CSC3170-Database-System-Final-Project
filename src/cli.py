# cli.py
import sys
from user import register_user
from user import login
from book import search_books, add_book
from transaction import borrow_book, return_book

def display_menu():
    """
    Displays the main menu options to the user.
    """
    print("Welcome to the Library Management System")
    print("1. Login")
    print("2. Register as Patron")
    print("3. Register as Librarian")
    print("4. Exit")

def register(role):
    """
    Handles the registration process for a new user.
    """
    print("\nRegister a new user")

    # Get username, password, and role from user
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    
    # Ask for role (patron or librarian)
    if role == '2':
        role = 'patron'
    elif role == '3':
        role = 'librarian'
    
    # Register the user
    register_user(username, password, role)
    
    print("Registration successful as a", role)

def main():
    """
    Main entry point for the CLI program.
    """
    while True:
        display_menu()
        choice = input("\nChoose an option: ")

        if choice == '1':
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            user = login(username, password)
            if user:
                print(f"Login Successful. Welcome, {username}!")
                role = user['role']
                while True:
                    if role == 'librarian':
                        print("1. Add a Book\n2. Search Books\n3. Exit")
                        choice = input("Choose an option: ")
                        if choice == '1':
                            title = input("Enter book title: ")
                            author = input("Enter author: ")
                            genre = input("Enter genre: ")
                            availability = 1  # Book available
                            add_book(title, author, genre, availability)
                            print("Book added successfully.")
                        elif choice == '2':
                            query = input("Enter search query (title): ")
                            books = search_books(query)
                            if books:
                                for book in books:
                                    print(f"Book ID: {book['book_id']}, Title: {book['title']}")
                            else:
                                print("No books found.")
                        elif choice == '3':
                            sys.exit()
                    elif role == 'patron':
                        print("1. Borrow Book\n2. Return Book\n3. Search Books\n4. Exit")
                        choice = input("Choose an option: ")
                        if choice == '1':
                            book_id = int(input("Enter Book ID to borrow: "))
                            borrow_book(user['user_id'], book_id)
                            print("Book borrowed successfully.")
                        elif choice == '2':
                            book_id = int(input("Enter Book ID to return: "))
                            return_book(user['user_id'], book_id)
                            print("Book returned successfully.")
                        elif choice == '3':
                            query = input("Enter search query (title): ")
                            books = search_books(query)
                            for book in books:
                                print(f"Book ID: {book['book_id']}, Title: {book['title']}")
                        elif choice == '4':
                            sys.exit()
                    else:
                        print("Invalid role.")
            else:
                print("Invalid username or password.")
        
        elif choice == '2' or choice == '3':
            register(choice)  # Register as patron or librarian
        
        
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
