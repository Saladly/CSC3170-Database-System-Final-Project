# cli.py
import sys
from user import register_user, login, pre_register_admin
from book import search_books, add_book
from transaction import (
    borrow_book,
    return_book,
    generate_report,
    view_personal_history,
    view_due_dates,
    renew_book,
    view_book_popularity,
    check_overdue_books,
    calculate_fines,
    show_fines,
    view_fines,
    give_feedback,
    get_top_rated_books
)

def display_menu():
    # Displays the main menu options to the user.
    print("\n" + "="*50)
    print("Welcome to the Library Management System".center(50))
    print("="*50 + "\n")
    print("1. Login".center(50))
    print("2. Register as Patron".center(50))
    print("3. Exit".center(50))
    print("\n" + "="*50)

def admin_menu():
    # Menu displayed only to admin users after login.
    print("\n" + "="*50)
    print("Admin Menu".center(50))
    print("="*50 + "\n")
    print("1. Add a Book".center(50))
    print("2. Search Books".center(50))
    print("3. Generate Report".center(50))
    print("4. Register Librarian".center(50))
    print("5. View Book Popularity".center(50))
    print("6. Check Overdue".center(50))
    print("7. Calculate Fines".center(50))
    print("8. Show Fines".center(50))
    print("9. View Top Rated Books".center(50))
    print("10. Exit".center(50))
    print("\n" + "="*50)

def patron_menu():
    # Menu displayed only to patron users after login.
    print("\n" + "="*50)
    print("Patron Menu".center(50))
    print("="*50 + "\n")
    print("1. Borrow Book".center(50))
    print("2. Return Book".center(50))
    print("3. Search Books".center(50))
    print("4. View Transaction History".center(50))
    print("5. View Due Dates".center(50))
    print("6. Renew Book".center(50))
    print("7. View and Pay Fines".center(50))
    print("8. Give Feedback".center(50))
    print("9. Exit".center(50))
    print("\n" + "="*50)
    
def register(role, admin_user=None):
    # Handles the registration process for a new user.
    print("\n" + "-"*50)
    print("Register a new user".center(50))
    print("-"*50)

    # Get username, password, and role from user
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    
    # Check for role (patron or librarian)
    if role == '2':
        role = 'patron'
    elif role == '3':
        role = 'librarian'

    # Register the user
    register_user(username, password, role, admin_user)
    
    if role == 'librarian':
        print("Librarian registration successful.")
        
# Main function to run the program
def main():
    # Variable to store admin user during session
    admin_user = None  

    # Ensure admin account exists
    pre_register_admin()  

    while True:
        display_menu()
        choice = input("\nChoose an option: ")

        if choice == '1':
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            user = login(username, password)
            if user:
                print("\n" + "="*50)
                print(f"Login Successful. Welcome, {username}!".center(50))
                print("="*50)
                role = user['role']
                # Store logged-in user as admin_user if admin
                admin_user = user  

                if role == 'librarian':
                    while True:
                        # Show admin menu to admin users
                        admin_menu()  
                        choice = input("Choose an option: ")
                        if choice == '1':
                            title = input("Enter book title: ")
                            author = input("Enter author: ")
                            genre = input("Enter genre: ")
                            # Start with all books available
                            availability = 1  
                            add_book(title, author, genre, availability)
                            print("\n" + "-"*50)
                            print("Book added successfully.".center(50))
                            print("-"*50)
                        elif choice == '2':
                            # Search Books
                            print("\n" + "-"*50)
                            print("Search Books".center(50))
                            print("-"*50 + "\n")
                            print("1. Search by Title".center(50))
                            print("2. Search by Author".center(50))
                            search_choice = input("\nChoose an option: ")
                            if search_choice == '1':
                                query = input("Enter title to search: ")
                                books = search_books(query, search_type='title')
                            elif search_choice == '2':
                                query = input("Enter author to search: ")
                                books = search_books(query, search_type='author')
                            else:
                                print("Invalid choice.")
                                continue
                            if books:
                                print("\n" + "-"*50)
                                print("Search Results".center(50))
                                print("-"*50)
                                for book in books:
                                    availability = 'Available' if book['availability'] else 'Not Available'
                                    print(f"Book ID: {book['book_id']}, Title: '{book['title']}', Author: {book['author']}, Availability: {availability}")
                                print("-"*50)
                            else:
                                print("No books found.")
                        elif choice == '3':
                            # Generate report for librarian
                            generate_report() 
                        elif choice == '4':
                            print("Registering new librarian...")
                            register('3', admin_user)
                        elif choice == '5':
                            view_book_popularity()
                        elif choice == '6':
                            check_overdue_books()
                        elif choice == '7':
                            calculate_fines()
                        elif choice == '8':
                            show_fines()
                        elif choice == '9':
                            get_top_rated_books()
                        elif choice == '10':
                            print("\n" + "="*50)
                            print("Goodbye!".center(50))
                            print("="*50)
                            sys.exit()
                        else:
                            print("Invalid choice. Please try again.")
                elif role == 'patron':
                    while True:
                        # Show patron menu to patron users
                        patron_menu()  
                        choice = input("Choose an option: ")
                        if choice == '1':
                            book_id = int(input("Enter Book ID to borrow: "))
                            borrow_book(user['user_id'], book_id)
                        elif choice == '2':
                            book_id = int(input("Enter Book ID to return: "))
                            return_book(user['user_id'], book_id)
                        elif choice == '3':
                            # Search Books
                            print("\n" + "-"*50)
                            print("Search Books".center(50))
                            print("-"*50 + "\n")
                            print("1. Search by Title".center(50))
                            print("2. Search by Author".center(50))
                            search_choice = input("\nChoose an option: ")
                            if search_choice == '1':
                                query = input("Enter title to search: ")
                                books = search_books(query, search_type='title')
                            elif search_choice == '2':
                                query = input("Enter author to search: ")
                                books = search_books(query, search_type='author')
                            else:
                                print("Invalid choice.")
                                continue
                            if books:
                                print("\n" + "-"*50)
                                print("Search Results".center(50))
                                print("-"*50)
                                for book in books:
                                    availability = 'Available' if book['availability'] else 'Not Available'
                                    print(f"Book ID: {book['book_id']}, Title: '{book['title']}', Author: {book['author']}, Availability: {availability}")
                                print("-"*50)
                            else:
                                print("No books found.")
                            pass
                        elif choice == '4':
                            # View Transaction History
                            view_personal_history(user['user_id'])
                        elif choice == '5':
                            view_due_dates(user['user_id'])
                        elif choice == '6':
                            book_id = int(input("Enter Book ID to renew: "))
                            renew_book(user['user_id'], book_id)
                        elif choice == '7':
                            view_fines(user['user_id'])
                        elif choice == '8':
                            give_feedback(user['user_id'])
                        elif choice == '9':
                            print("\n" + "="*50)
                            print("Goodbye!".center(50))
                            print("="*50)
                            sys.exit()
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("Invalid role.")
            else:
                print("Invalid username or password.")
        
        elif choice == '2':
            # Register as patron
            register(choice)  
        
        elif choice == '3':
            print("\n" + "="*50)
            print("Exiting the system. Goodbye!".center(50))
            print("="*50)
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
