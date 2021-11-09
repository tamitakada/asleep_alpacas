import sqlite3

# from flask import Flask

DB_FILE="database.db"

###############
#             #
# Basic Setup #
#             #
###############

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

# Create tables if they don't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS stories (
      id INTEGER PRIMARY KEY,
      author_id INTEGER,
      title TEXT,
      full_story TEXT,
      last_update TEXT
    )""")
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      username TEXT,
      password TEXT
    )""")
c.execute("""
    CREATE TABLE IF NOT EXISTS contributions (
      user_id INTEGER,
      story_id INTEGER
    )""")
# c.execute("INSERT INTO users VALUES (1, 'justin', 'story')")
# for i,j in c.execute('SELECT username, password FROM users'):
#     print (i)
#     print (j)
#test code

# Save and close

db.commit()
db.close()
#####################
#                   #
# Utility Functions #
#                   #
#####################


def fetch_user_id(username, password):
    """
    Gets the id of the user with the given username/password combination from the database.
    Returns None if the combination is incorrect.
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
        SELECT id
        FROM   users
        WHERE  username = ?
        AND    password = ?
    """, (username, password))

    # user_id is None if no matches were found
    user_id = c.fetchone()

    db.close()

    return user_id


def register_user(username, password):
    """
    Tries to add the given username and password into the database.
    Returns False if the user already exists, True if it successfully added the user.
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    for i in c.execute('SELECT username FROM users'):
        if i[0] == username:
            return False
    c.execute("""INSERT INTO users(username,password) VALUES(?, ?)""",(username,password))
    db.commit()
    db.close()
    return True


def fetch_username(user_id):
    """
    Returns the username of the user with the given id.
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    username = c.fetchone()

    db.close()
    return username


def has_user_contributed(user_id, story_id):
    """
    Returns whether or not the given user_id has contributed to the story_id.
    """

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
        SELECT *
        FROM   contributions
        WHERE  user_id = ?
             AND story_id = ?
    """, (user_id, story_id))
    data = c.fetchone()

    db.close()
    return data is not None


def fetch_story(story_id):
    """
    Returns a dictionary containing the information of the story with the given id.
    NOTE: It actually returns a sqlite3.Row, which is a tuple dictionary hybrid.
          For all intents and purposes though, it can be treated as a dictionary.
    """
    db = sqlite3.connect(DB_FILE)

    # This just makes turns the rows into dictionary-like objects instead of the plain tuples
    # I highly recommend reading more about it in the docs:
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
    db.row_factory = sqlite3.Row
    c = db.cursor()

    c.execute("SELECT * FROM stories WHERE id = ?", (story_id,))
    story = c.fetchone()

    db.commit()
    db.close()

    return story

def fetch_all_stories():
    """
    Same as fetch_story but returns a list of all stories in the database rather than just one.
    """
    db = sqlite3.connect(DB_FILE)

    # This just makes turns the rows into dictionary-like objects instead of the plain tuples
    # I highly recommend reading more about it in the docs:
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
    db.row_factory = sqlite3.Row
    c = db.cursor()

    c.execute("SELECT * FROM stories")
    stories = c.fetchall()

    db.close()

    return stories

def fetch_contributions(contributor_id):
    """
    Same as fetch_all_stories but only returns the stories the the contributor has contributed to.
    """
    db = sqlite3.connect(DB_FILE)

    # This just makes turns the rows into dictionary-like objects instead of the plain tuples
    # I highly recommend reading more about it in the docs:
    # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
    db.row_factory = sqlite3.Row
    c = db.cursor()

    # Selects the stories where the id is one of the contributions made by a user with the given id
    c.execute("""
        SELECT *
        FROM stories
        WHERE id in (SELECT story_id
                     FROM contributions
                     WHERE user_id = ?)
    """, (contributor_id,))
    stories = c.fetchall()

    db.close()

    return stories

def create_story(author_id, title, body):
    """
    Adds a story to the database with the appropriate information.
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
        INSERT INTO stories(author_id,
                            title,
                            full_story,
                            last_update)
        VALUES(?, ?, ?, ?)
    """,(author_id, title, body, body))

    story_id = c.lastrowid
    c.execute("INSERT INTO contributions(user_id,story_id) VALUES(?,?)",(author_id,story_id))

    db.commit()
    db.close()

def append_to_story(contributor_id, story_id, content):
    """
    Adds to the story.
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
        SELECT full_story
        FROM stories
        WHERE id = ?
    """, story_id)
    full_story, = c.fetchone()

    if full_story is None:
        c.close()
        return

    full_story += content
    c.execute("""
        UPDATE stories
        SET full_story = ?
          , last_update = ?
        WHERE id = ?
    """, (full_story, content, story_id))

    c.execute("INSERT INTO contributions(user_id,story_id) VALUES(?,?)",(contributor_id,story_id))

    db.commit()
    db.close()
