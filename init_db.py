import sqlite3

# Connect to the database (will create it if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT,
    email TEXT,
    hashed_password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database initialized and 'users' table created.")
