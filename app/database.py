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
             , password = ?
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
             , story_id = ?
    """, (user_id, story_id))
    data = c.fetchone()

    db.commit()
    db.close()

    return data is not None


def fetch_story(story_id):
    """
    Returns a dictionary containing the information of the story with the given id.
    """
`
    # TODO: implementationusername


def fetch_story_ids(contributor_id = None):
    """
    If contributor_id is None, return a list of all stories' ids.
    If a contributer_id is given, return a list of all of their contributions' ids.
    """

    # TODO: implementation

    return []

def create_story(author_id, title, body):
    """
    Adds a story to the database with the appropriate information.
    """
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""INSERT INTO stories(title,body) VALUES(?, ?)""",(title,body))
    db.commit()
    db.close()
    # TODO: implementation

def append_to_story(contributor_id, story_id, content):
    """
    Adds to the
    """

    # TODO: implementation
