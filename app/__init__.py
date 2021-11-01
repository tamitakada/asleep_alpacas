from flask import Flask, request, redirect, render_template, session, request

app = Flask(__name__)

@app.route("/")
def home():
    return "home"

@app.route("/logout")
def logout():
    print("logout page...redirecting to homepage")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check login
        if "username" in request.form:
            session["user"] = request.form["username"]
        return redirect("/")
    else:
        # Display login page
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Try to register account
        return redirect("/")
    else:
        # Display register page
        return "register"

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # Add story to database
        return redirect("/")
    else:
        # Display create page
        return "create"

@app.route("/discover")
def discover():
    return "discover"

@app.route("/story/<story_id>", methods=["GET", "POST"])
def story(story_id):
    """
    Using angle brackets in the route means it'll pass the value
    of it as a parameter to the function
    """

    user_has_contributed = True # placeholder variable

    if user_has_contributed:
        # Display full story
        return f"story with id of {story_id}"
    elif request.method == "POST":
        # Add to story
        # Display full story
        return f"story with id of {story_id}"
    else:
        # Display edit page
        return "edit"

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "It's Rewind Time"
    app.run()
