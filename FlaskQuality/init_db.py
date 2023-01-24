import sqlite3

connection = sqlite3.connect('users.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Here we insert these values to have a basis
# Notice ('First post' and 'content for the first post' this is meant to be replaced)

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

cur.execute("INSERT INTO admin (username, email, password) VALUES (?, ?, ?)",
            ('admin', 'admin', 'password')
            )

# Create user info table

cur.execute(
    'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)')

connection.commit()

cur.row_factory = sqlite3.Row

connection.close()
