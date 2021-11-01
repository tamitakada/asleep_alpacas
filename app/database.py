import sqlite3

DB_FILE="database.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

c.execute("CREATE TABLE courses (id INTEGER, author_id INTEGER, title TEXT, full_story TEXT, last_update TEXT)")
#view Story
c.execute("CREATE TABLE courses (id INTEGER, username TEXT, password TEXT)")
#users
c.execute("CREATE TABLE courses (user_id INTEGER, story_id INTEGER)")
#edit story
