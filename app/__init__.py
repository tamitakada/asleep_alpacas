from flask import Flask, request, redirect, render_template, session, request

app = Flask(__name__)

def is_logged_in():
    return "user" in session

@app.route("/")
def home():
    if is_logged_in():
        return f"home -- welcome, {session['user']}"

    return "home"

@app.route("/logout")
def logout():
    print("logout page...redirecting to homepage")
    if is_logged_in():
        session.pop("user")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect("/")
    if request.method == 'GET':
        # Check login
        if "username" in request.args and "password" in request.args:
            session["user"] = request.args["username"]
            pas = request.args['password']
    if request.method == "POST":
        # Check login
        if "username" in request.form and "password" in request.form:
            session["user"] = request.form["username"]
            pas = request.args['password']
    #verify this user and password exists
    #try:
    #    if database.fetch_user_id(session["user"],  pas) == None:
                        
    #except:
    #   return render_template('login.html', explain="seems like something went wrong! try again")
    else:
        # Display login page
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if is_logged_in():
        return redirect("/")

    if request.method == "POST":
        # Try to register account
        return redirect("/")
    else:
        # Display register page
        return "register"

@app.route("/create", methods=["GET", "POST"])
def create():
    if not is_logged_in():
        return "You must be logged in!"

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
