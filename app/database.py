import sqlite3

from flask import sessions
import __init__

DB_FILE="database.db"
id = 0
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXIST Stories (id INTEGER, author_id INTEGER, title TEXT, full_story TEXT, last_update TEXT)")
#view Story
c.execute("CREATE TABLE IF NOT EXIST users (id INTEGER, username TEXT, password TEXT)")
if __init__.is_logged_in():
    id = id + 1
    command = f"""
            INSERT INTO users VALUES
              ({id},
              {repr(sessions['user'])}
              {repr(sessions['user'])})
        """
    c.execute(command);
#users
c.execute("CREATE TABLE IF NOT EXIST contributors (user_id INTEGER, story_id INTEGER)")
#edit story
db.commit()
db.close() 
