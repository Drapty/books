import sqlite3  


##connect to sql 


conn = sqlite3.connect('media_collection.db')
##comnicateor interact with the database
cursor= conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    genre TEXT NOT NULL,
    rating TEXT,
    review TEXT,
    date_added DATE DEFAULT CURRENT_DATE NOT NULL
)
""")