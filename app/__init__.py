from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "home"

@app.route("/logout")
def logout():
    return "logout"

@app.route("/login")
def login():
    return "login"

@app.route("/register")
def register():
    return "register"

@app.route("/create")
def create():
    return "create"

@app.route("/discover")
def discover():
    return "discover"

@app.route("/story/<story_id>")
def story(story_id):
    """
    Using angle brackets in the route means it'll pass the value
    of it as a parameter to the function
    """
    return f"story with id of {story_id}"

if __name__ == "__main__":
    app.debug = True
    app.run()
