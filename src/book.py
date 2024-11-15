from db import execute_query, fetch_results

def add_book(title, author, genre, availability):
    query = "INSERT INTO Books (title, author, genre, availability) VALUES (%s, %s, %s, %s)"
    execute_query(query, (title, author, genre, availability))

def search_books(query_string):
    query = "SELECT * FROM Books WHERE title LIKE %s"
    return fetch_results(query, ('%' + query_string + '%',))

def update_book_availability(book_id, availability):
    query = "UPDATE Books SET availability = %s WHERE book_id = %s"
    execute_query(query, (availability, book_id))
