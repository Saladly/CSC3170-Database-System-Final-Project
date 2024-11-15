import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ELSANNAly123..",
        database="library_system"
    )