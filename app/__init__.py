from flask import Flask, request, redirect, render_template, session, request
import database

app = Flask(__name__)

def is_logged_in():
    return "user" in session

@app.route("/")
def home():
    if is_logged_in():
        return f"home -- welcome, {session['user']}"

    return render_template('home.html')

@app.route("/logout")
def logout():
    print("logout page...redirecting to homepage")
    if is_logged_in():
        session.pop("user")
        session.pop("user_id")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    try: 
        if is_logged_in():
            return redirect("/")
        if request.method == 'GET':
            # Check login
            if "username" in request.args and "password" in request.args:
                username = request.args["username"]
                pas = request.args["password"]
        if request.method == "POST":
            # Check login
            if "username" in request.form and "password" in request.form:
                username = request.form["username"]
                pas = request.form["password"]

        # verify this user and password exists
        user_id = database.fetch_user_id(username, pas)
        if user_id is not None:
            # Adds user and user id to session
            session["user"] = username
            session["user_id"] = user_id
            return redirect("/")
        # if it doesn't, return to home
        else:
            return render_template('login.html', explain = "login information is wrong")
    except:
        return render_template('login.html')
    
    #except:
    #   return render_template('login.html', explain=
    # "seems like something went wrong! check your username and password combination! you may also make a new account")

@app.route("/register", methods=["GET", "POST"])
def register():
    if is_logged_in():
        return render_template('home.html')
    if "newusername" in request.args and "newpassword" in request.args:
        if request.method == 'GET':
            # Check login
            if database.register_user(request.args["newusername"], request.args["newpassword"]) == False:
                return render_template('register.html', explain = "username already exists")
            #if username doesn't exist, the account is created and sent to login page
            else:
                return render_template('login.html')
        if request.method == 'POST':
            # Check login
            if database.register_user(request.form["newusername"], request.form["newpassword"]) == False:
                return render_template('register.html', explain = "username already exists or wrong values entered")
            #if username doesn't exist, the account is created and sent to login page
            else:
                return render_template('login.html')
    #if not, stay on login page
    else:
        return render_template('register.html')

@app.route("/create", methods=["GET", "POST"])
def create():
    if not is_logged_in():
        return "You must be logged in!"

    if request.method == "POST":
        # Add story to database
        user_id = session["user_id"]
        database.create_story(user_id, "[placeholder_title]", "[placeholder_body]")
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
    if not is_logged_in():
        return "You must be logged in!"

    user_id = session["user_id"]

    if has_user_contributed(user_id, story_id):
        # Display full story
        return f"story with id of {story_id}"
    elif request.method == "POST":
        # Add to story
        # Display full story
        append_to_story(user_id, story_id, "[placeholder_content]")
        return f"story with id of {story_id}"
    else:
        # Display edit page
        return "edit"

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "It's Rewind Time"
    app.run()
