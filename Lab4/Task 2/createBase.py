import sys
import hashlib
import sqlite3

db = sqlite3.connect('Lab-database.db')

cursor = db.cursor()

cursor.execute("""CREATE TABLE author (
    idAuthor text,
    name text,
    country text,
    years text
)""")

cursor.execute("""CREATE TABLE books (
    idAuthor text,
    name text,
    size text,
    publishing text,
    yearsPublishing text
)""")

cursor.execute("""CREATE TABLE users (
    id text,
    login text,
    password text
)""")

db.commit()

db.close()

