from db import execute_query

def borrow_book(user_id, book_id):
    query = "UPDATE Books SET availability = 0 WHERE book_id = %s AND availability = 1"
    execute_query(query, (book_id,))
    query = "INSERT INTO Transactions (user_id, book_id, action, transaction_date) VALUES (%s, %s, 'borrow', NOW())"
    execute_query(query, (user_id, book_id))

def return_book(user_id, book_id):
    query = "UPDATE Books SET availability = 1 WHERE book_id = %s"
    execute_query(query, (book_id,))
    query = "INSERT INTO Transactions (user_id, book_id, action, transaction_date) VALUES (%s, %s, 'return', NOW())"
    execute_query(query, (user_id, book_id))
