import sqlite3

from flask import sessions

DB_FILE="database.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

# Create tables if they don't exist
c.execute("CREATE TABLE IF NOT EXIST stories (id INTEGER, author_id INTEGER, title TEXT, full_story TEXT, last_update TEXT)")
c.execute("CREATE TABLE IF NOT EXIST users (id INTEGER, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXIST contributions (user_id INTEGER, story_id INTEGER)")

db.commit()
db.close() 
