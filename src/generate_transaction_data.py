# generate_transactions.py

from db import execute_query, fetch_results
import random
from datetime import datetime, timedelta
import sys
import os

def generate_random_date_within_last_year():
    # Generates a random datetime within the last year from today.
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    # Generate a random number of seconds between one_year_ago and today
    random_seconds = random.randint(0, int((today - one_year_ago).total_seconds()))
    random_date = one_year_ago + timedelta(seconds=random_seconds)
    return random_date

def generate_transactions(num_transactions):
    # Generates and inserts transactions into the database with realistic transaction and due dates.
    # Each 'borrow' is paired with a 'return' within 10 days.
    # Fetch all patron user_ids and book_ids
    patrons = fetch_results("SELECT user_id FROM Users WHERE role = 'patron'")
    books = fetch_results("SELECT book_id FROM Books")
    patron_ids = [patron['user_id'] for patron in patrons]
    book_ids = [book['book_id'] for book in books]
    
    actions = ['borrow', 'return']
    
    for _ in range(num_transactions):
        user_id = random.choice(patron_ids)
        book_id = random.choice(book_ids)
        
        # Generate a random transaction_date within the last year for 'borrow'
        borrow_date = generate_random_date_within_last_year()
        due_date = borrow_date + timedelta(days=10)
        
        # Insert 'borrow' transaction
        borrow_query = """
        INSERT INTO Transactions (user_id, book_id, action, transaction_date, due_date)
        VALUES (%s, %s, 'borrow', %s, %s)
        """
        execute_query(borrow_query, (user_id, book_id, borrow_date, due_date))
        
        # Update book availability to 0 (not available)
        update_borrow_query = "UPDATE Books SET availability = 0 WHERE book_id = %s"
        execute_query(update_borrow_query, (book_id,))
        
        # Generate a random return_date between borrow_date and due_date
        delta_seconds = int((due_date - borrow_date).total_seconds())
        random_seconds = random.randint(1, delta_seconds)
        return_date = borrow_date + timedelta(seconds=random_seconds)
        
        # Insert 'return' transaction
        return_query = """
        INSERT INTO Transactions (user_id, book_id, action, transaction_date, due_date)
        VALUES (%s, %s, 'return', %s, NULL)
        """
        execute_query(return_query, (user_id, book_id, return_date))
        
        # Update book availability to 1 (available)
        update_return_query = "UPDATE Books SET availability = 1 WHERE book_id = %s"
        execute_query(update_return_query, (book_id,))
    
    print(f"{num_transactions} transactions (borrow and return pairs) have been added to the database.")

if __name__ == "__main__":
    generate_transactions(4000)
