# transaction.py
from db import fetch_results, execute_query
from book import get_book_by_id
from datetime import datetime, timedelta

def borrow_book(user_id, book_id):
    # Allows a patron to borrow a book if it's available.
    # Get book details
    book = get_book_by_id(book_id)
    if not book:
        print("Book not found.")
        return
    if not book['availability']:
        print(f"The book '{book['title']}' by {book['author']} is currently not available.")
        return
    # Proceed to borrow the book
    update_query = "UPDATE Books SET availability = 0 WHERE book_id = %s"
    execute_query(update_query, (book_id,))
    # Set due date to 10 days from now
    due_date = datetime.now() + timedelta(days=10)
    transaction_query = """
    INSERT INTO Transactions (user_id, book_id, action, transaction_date, due_date)
    VALUES (%s, %s, 'borrow', NOW(), %s)
    """
    execute_query(transaction_query, (user_id, book_id, due_date))
    print(f"You have successfully borrowed '{book['title']}' by {book['author']}. Due date is {due_date.strftime('%Y-%m-%d %H:%M:%S')}.")

def return_book(user_id, book_id):
    # Allows a patron to return a book if they have borrowed it.
    # Get book details
    book = get_book_by_id(book_id)
    if not book:
        print("Book not found.")
        return
    # Check if the user has borrowed this book
    check_query = """
    SELECT action FROM Transactions
    WHERE user_id = %s AND book_id = %s
    ORDER BY transaction_date DESC LIMIT 1
    """
    result = fetch_results(check_query, (user_id, book_id))
    if not result or result[0]['action'] != 'borrow':
        print("You have not borrowed this book.")
        return
    # Proceed to return the book
    update_query = "UPDATE Books SET availability = 1 WHERE book_id = %s"
    execute_query(update_query, (book_id,))
    transaction_query = "INSERT INTO Transactions (user_id, book_id, action, transaction_date) VALUES (%s, %s, 'return', NOW())"
    execute_query(transaction_query, (user_id, book_id))
    print(f"You have successfully returned '{book['title']}' by {book['author']}.")

def generate_report():
    # Generates a report of all transactions.
    # Admins can use this to see all borrow/return transactions.
    query = """
    SELECT t.transaction_id, u.username, b.title, t.action, t.transaction_date 
    FROM Transactions t
    JOIN Users u ON t.user_id = u.user_id
    JOIN Books b ON t.book_id = b.book_id
    ORDER BY t.transaction_date DESC;
    """
    transactions = fetch_results(query)
    
    if transactions:
        print("\nTransaction Report:")
        for t in transactions:
            print(f"Transaction ID: {t['transaction_id']}, User: {t['username']}, Book: {t['title']}, Action: {t['action']}, Date: {t['transaction_date']}")
    else:
        print("No transactions found.")
        
def view_personal_history(user_id):
    # Allows a patron to view their personal transaction history.
    query = """
    SELECT t.transaction_id, b.book_id, b.title, t.action, t.transaction_date
    FROM Transactions t
    JOIN Books b ON t.book_id = b.book_id
    WHERE t.user_id = %s
    ORDER BY t.transaction_date DESC;
    """
    history = fetch_results(query, (user_id,))
    
    if history:
        print("\nYour Transaction History:")
        for record in history:
            print(f"Transaction ID: {record['transaction_id']}, Book ID: {record['book_id']}, Title: '{record['title']}', Action: {record['action']}, Date: {record['transaction_date']}")
    else:
        print("You have no transaction history.")

def view_book_popularity():
    # Displays the top 5 books that have been borrowed most frequently recently.
    # Define "recently" as the last 30 days
    query = """
    SELECT b.title, COUNT(*) as borrow_count
    FROM Transactions t
    JOIN Books b ON t.book_id = b.book_id
    WHERE t.action = 'borrow' AND t.transaction_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    GROUP BY t.book_id
    ORDER BY borrow_count DESC
    LIMIT 5;
    """
    results = fetch_results(query)
    
    if results:
        print("\nTop 5 Most Borrowed Books in the Last 30 Days:")
        for idx, book in enumerate(results, 1):
            print(f"{idx}. '{book['title']}' - Borrowed {book['borrow_count']} times")
    else:
        print("No borrowing activity in the last 30 days.")
        
def view_due_dates(user_id):
    # Allows a patron to view their borrowed books with due dates.
    query = """
    SELECT t.transaction_id, b.title, t.transaction_date, t.due_date
    FROM Transactions t
    JOIN Books b ON t.book_id = b.book_id
    WHERE t.user_id = %s AND t.action = 'borrow' AND NOT EXISTS (
        SELECT 1 FROM Transactions t2
        WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return' AND t2.transaction_date > t.transaction_date
    )
    ORDER BY t.transaction_date DESC;
    """
    results = fetch_results(query, (user_id,))
    
    if results:
        print("\nYour Borrowed Books and Due Dates:")
        for record in results:
            overdue = ""
            due_date = record['due_date']
            if due_date and due_date < datetime.now():
                overdue = " (Overdue)"
            print(f"Book: '{record['title']}', Borrowed on: {record['transaction_date']}, Due on: {due_date}{overdue}")
    else:
        print("You have no borrowed books with due dates.")
        
def renew_book(user_id, book_id):
    # Allows a patron to renew a borrowed book, extending the due date by 10 days.
    # Check if the user has borrowed this book and hasn't returned it
    query = """
    SELECT t.transaction_id, t.due_date
    FROM Transactions t
    WHERE t.user_id = %s AND t.book_id = %s AND t.action = 'borrow' AND NOT EXISTS (
        SELECT 1 FROM Transactions t2
        WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return' AND t2.transaction_date > t.transaction_date
    )
    ORDER BY t.transaction_date DESC LIMIT 1
    """
    result = fetch_results(query, (user_id, book_id))
    if not result:
        print("You have not borrowed this book or have already returned it.")
        return
    # Proceed to renew the book
    transaction_id = result[0]['transaction_id']
    current_due_date = result[0]['due_date']
    if current_due_date is None:
        print("This book does not have a due date.")
        return
    new_due_date = current_due_date + timedelta(days=10)
    update_query = "UPDATE Transactions SET due_date = %s WHERE transaction_id = %s"
    execute_query(update_query, (new_due_date, transaction_id))
    book_title = get_book_by_id(book_id)['title']
    print(f"The due date for '{book_title}' has been extended to {new_due_date.strftime('%Y-%m-%d %H:%M:%S')}.")
    
def check_overdue_books():
    # Allows librarians to view all users who have overdue books.
    query = """
    SELECT 
        t.user_id, u.username, t.book_id, b.title, t.due_date, DATEDIFF(NOW(), t.due_date) AS days_overdue
    FROM 
        Transactions t
    JOIN 
        Users u ON t.user_id = u.user_id
    JOIN 
        Books b ON t.book_id = b.book_id
    WHERE 
        t.action = 'borrow' AND 
        t.due_date < NOW() AND 
        NOT EXISTS (
            SELECT 1 FROM Transactions t2
            WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return' AND t2.transaction_date > t.transaction_date
        )
    ORDER BY 
        t.due_date ASC;
    """
    overdue_records = fetch_results(query)
    
    if overdue_records:
        print("\nOverdue Books:")
        for record in overdue_records:
            print(f"User ID: {record['user_id']}, Username: {record['username']}")
            print(f"Book ID: {record['book_id']}, Title: '{record['title']}'")
            print(f"Due Date: {record['due_date']}, Days Overdue: {record['days_overdue']}")
            print("-" * 50)
    else:
        print("There are no overdue books at this time.")
        

def calculate_fines():
    # Calculates fines for overdue transactions and inserts them into the Fines table.
    query = """
    SELECT t.transaction_id, t.user_id, t.book_id, t.due_date, DATEDIFF(NOW(), t.due_date) AS days_overdue
    FROM Transactions t
    WHERE t.action = 'borrow' AND t.due_date < NOW()
    AND NOT EXISTS (
        SELECT 1 FROM Transactions t2
        WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return' AND t2.transaction_date > t.transaction_date
    )
    AND NOT EXISTS (
        SELECT 1 FROM Fines f
        WHERE f.transaction_id = t.transaction_id AND f.is_paid = 0
    )
    """
    overdue_transactions = fetch_results(query)
    if overdue_transactions:
        for transaction in overdue_transactions:
            overdue_days = transaction['days_overdue']
            # 5 yuan per day of overdue
            fine_amount = overdue_days * 5  
            insert_query = """
            INSERT INTO Fines (user_id, book_id, transaction_id, overdue_days, fine_amount, is_paid)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            execute_query(insert_query, (transaction['user_id'], transaction['book_id'], transaction['transaction_id'], overdue_days, fine_amount, 0))
        print("Fines calculated and records inserted.")
        

    else:
        print("No new overdue transactions to calculate fines for.")
        
def show_fines():
    # Allows admin to view all fines with user name, book title, transaction date, and payment status.
    query = """
    SELECT f.fine_id, u.username, b.title, t.transaction_date, f.fine_amount, f.is_paid
    FROM Fines f
    JOIN Users u ON f.user_id = u.user_id
    JOIN Books b ON f.book_id = b.book_id
    JOIN Transactions t ON f.transaction_id = t.transaction_id
    ORDER BY f.date_issued DESC
    """
    fines = fetch_results(query)
    if fines:
        print("\nFine Records:")
        for fine in fines:
            status = 'Paid' if fine['is_paid'] else 'Unpaid'
            print(f"Fine ID: {fine['fine_id']}, User: {fine['username']}, Book: '{fine['title']}', Transaction Date: {fine['transaction_date']}, Amount: {fine['fine_amount']} yuan, Status: {status}")
    else:
        print("No fine records found.")

def view_fines(user_id):
    # Allows a patron to view their unpaid fines.
    query = """
    SELECT f.fine_id, b.title, f.overdue_days, f.fine_amount, f.is_paid
    FROM Fines f
    JOIN Books b ON f.book_id = b.book_id
    WHERE f.user_id = %s AND f.is_paid = 0
    """
    fines = fetch_results(query, (user_id,))
    if fines:
        print("\nYour Unpaid Fines:")
        total_fine = 0
        for fine in fines:
            print(f"Fine ID: {fine['fine_id']}, Book: '{fine['title']}', Overdue Days: {fine['overdue_days']}, Amount: {fine['fine_amount']} yuan")
            total_fine += fine['fine_amount']
        print(f"Total Fine Amount: {total_fine} yuan")
        pay = input("Do you want to pay all fines now? (yes/no): ")
        if pay.lower() == 'yes':
            pay_fine(user_id)
        else:
            print("You can pay your fines later.")
    else:
        print("You have no unpaid fines.")

def pay_fine(user_id):
    # Allows a patron to pay their unpaid fines.
    update_query = "UPDATE Fines SET is_paid = 1 WHERE user_id = %s AND is_paid = 0"
    execute_query(update_query, (user_id,))
    print("All your fines have been paid.")


def give_feedback(user_id):
    # Allows a patron to give feedback for a book.
    book_id = int(input("Enter Book ID to give feedback: "))
    # Check if user has borrowed this book
    query = """
    SELECT * FROM Transactions t
    WHERE t.user_id = %s AND t.book_id = %s AND t.action = 'borrow'
    """
    result = fetch_results(query, (user_id, book_id))
    if not result:
        print("You have not borrowed this book.")
        return
    # Check if user has already given feedback for this book
    check_query = "SELECT * FROM Feedback WHERE user_id = %s AND book_id = %s"
    feedback_exists = fetch_results(check_query, (user_id, book_id))
    if feedback_exists:
        print("You have already given feedback for this book.")
        return
    # Get feedback score
    while True:
        try:
            feedback_score = int(input("Enter your feedback score (0-10): "))
            if 0 <= feedback_score <= 10:
                break
            else:
                print("Please enter a number between 0 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 10.")
    # Insert feedback
    insert_query = "INSERT INTO Feedback (book_id, user_id, feedback_score) VALUES (%s, %s, %s)"
    execute_query(insert_query, (book_id, user_id, feedback_score))
    print("Thank you for your feedback!")

def get_top_rated_books():
    # Allows admin to view the top-rated 3 books.
    query = """
    SELECT b.title, AVG(f.feedback_score) as average_score
    FROM Feedback f
    JOIN Books b ON f.book_id = b.book_id
    GROUP BY f.book_id
    HAVING COUNT(f.feedback_id) > 2
    ORDER BY average_score DESC
    LIMIT 3
    """
    results = fetch_results(query)
    if results:
        print("\nTop 3 Rated Books:")
        for idx, book in enumerate(results, 1):
            print(f"{idx}. '{book['title']}' - Average Score: {book['average_score']:.2f}")
    else:
        print("No feedback records found.")