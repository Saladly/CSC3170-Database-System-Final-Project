# Used to generate date for database

import requests
from db import execute_query


def fetch_books_from_open_library(num_books):
    # Fetches book data from Open Library API and inserts into the database.
    base_url = 'http://openlibrary.org/search.json'
    params = {
        'q': 'the',  
        'limit': 100  
    }
    total_books = 0
    page = 1
    while total_books < num_books:
        params['page'] = page
        response = requests.get(base_url, params=params)
        data = response.json()
        books = data.get('docs', [])
        # No more books to fetch
        if not books:
            break  
        for book in books:
            if total_books >= num_books:
                break
            title = book.get('title', 'Unknown Title').replace("'", "''")
            author_list = book.get('author_name', ['Unknown Author'])
            author = author_list[0].replace("'", "''")
            genre_list = book.get('subject', ['General'])
            genre = genre_list[0].replace("'", "''")
            # Start with all books available
            availability = True 
            
            query = "INSERT INTO Books (title, author, genre, availability) VALUES (%s, %s, %s, %s)"
            execute_query(query, (title, author, genre, availability))
            total_books += 1
        # Move to the next page of results
        page += 1  
    print(f"{total_books} books have been added to the database from Open Library.")

# Fetch and insert 5000 books
fetch_books_from_open_library(5000)
