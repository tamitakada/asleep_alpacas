from flask import Flask, request, redirect, render_template, session
import database

app = Flask(__name__)

def is_logged_in():
    return "user" in session


@app.route("/")
def home():
    if is_logged_in():
        return render_template(
            "home.html",
            user=session["user"],
            stories=database.fetch_contributions(session["user_id"])
        )
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
    if is_logged_in():
        return redirect("/")

    # Default page
    if request.method == 'GET':
        return render_template("login.html")

    # Check login
    username = request.form["username"]
    pas = request.form["password"]

    if username.strip() == "" or pas.strip == "":
        return render_template('login.html', explain="please enter characters and/or numbers")
    
    # verify this user and password exists
    user_id = database.fetch_user_id(username, pas)
    if user_id is None:
        return render_template('login.html', explain="login information is wrong")

    # Adds user and user id to session
    session["user"] = database.fetch_username(user_id) # Ensures the displayed username is correct casing
    session["user_id"] = user_id
    return redirect("/")

    #except:
    #   return render_template('login.html', explain=
    # "seems like something went wrong! check your username and password combination! you may also make a new account")


@app.route("/register", methods=["GET", "POST"])
def register():
    if is_logged_in():
        return redirect("/")

    # Default page
    if request.method == "GET":
        return render_template('register.html')

    # Check login
    user = request.form["newusername"]
    pwd = request.form["newpassword"]
    if user.strip() == "" or pwd.strip == "":
        return render_template('register.html', explain="please enter characters and/or numbers")
    
    register_success = database.register_user(user, pwd)
    if not register_success:
        return render_template('register.html', explain="username already exists")

    return redirect("/login")


@app.route("/create", methods=["GET", "POST"])
def create():
    if not is_logged_in(): 
        return redirect("/login")

    # Default page
    if request.method == "GET":
        return render_template("new.html", user=session["user"])

    # Add story to database
    user_id = session["user_id"]
    title = request.form["Title"]
    body = request.form["Text"]
    database.create_story(user_id, title, body)
    return redirect("/")


@app.route("/discover")
def discover():
    return render_template(
        "discover.html",
        user=session.get("user"),
        stories=database.fetch_all_stories()
    )


@app.route("/story/<story_id>", methods=["GET", "POST"])
def story(story_id):
    """
    Using angle brackets in the route means it'll pass the value
    of it as a parameter to the function
    """
    if not is_logged_in():
        return redirect("/login")

    user_id = session["user_id"]

    if request.method == "POST":
        # Add to story
        # Display full story
        new_content = request.form["Text"]
        database.append_to_story(user_id, story_id, " " + new_content)

    story = database.fetch_story(story_id)
    if story is None:
        return redirect("/")

    author = database.fetch_username(story["author_id"])
    if database.has_user_contributed(user_id, story_id):
        # Display full story
        return render_template(
            "view.html",
            user=session["user"],
            story=story,
            explain = "You can no longer contribute to the story now"
        )
    else:
        # Display edit page
        return render_template(
            "edit.html",
            user=session["user"],
            story=story
        )

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "It's Rewind Time"
    app.run()
