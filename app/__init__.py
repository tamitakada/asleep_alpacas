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

        if username.strip() != "" and pas.strip != "":
            # verify this user and password exists
            user_id = database.fetch_user_id(username, pas)
            if user_id is not None:
                # Adds user and user id to session
                session["user"] = username
                session["user_id"] = user_id
                return redirect("/")
            else:
                return render_template('login.html', explain="login information is wrong")
        else:
            return render_template('login.html', explain="please enter characters and/or numbers")
    except:
        return render_template('login.html')

    #except:
    #   return render_template('login.html', explain=
    # "seems like something went wrong! check your username and password combination! you may also make a new account")

@app.route("/register", methods=["GET", "POST"])
def register():
    if is_logged_in():
        return redirect("/")

    if "newusername" in request.form and "newpassword" in request.form:
        if request.method == 'POST':
            #button to redirect to login page
            # if request.form.get("login"):
            #    return render_template("login.html")
            # Check login
            user = ""
            user = request.form["newusername"]
            pwd = ""
            pwd = request.form["newpassword"]
            if user.strip() != "" or pwd.strip != "":
                if database.register_user(user, pwd) == False:
                    return render_template('register.html', explain="username already exists")
                #if username doesn't exist, the account is created and sent to login page
                else:
                    return redirect("/login")
            else:
                return render_template('register.html', explain="please enter characters and/or numbers")

    return render_template('register.html')

@app.route("/create", methods=["GET", "POST"])
def create():
    if is_logged_in(): 
        if request.method == "POST":
            # Add story to database
            #user_id = session["user"]
            user_id = session["user_id"]
            title = request.form["Title"]
            body = request.form["Text"]
            database.create_story(user_id, title, body)
            return redirect("/")
        else:
            return render_template("new.html", user=session["user"])
    else:
        return redirect("/login")


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
            title=story["title"],
            author=author,
            body=story["full_story"],
            explain = "You can no longer contribute to the story now"
            
        )
    else:
        # Display edit page
        return render_template(
            "edit.html",
            user=session["user"],
            title=story["title"],
            author=author,
            last_update=story["last_update"]
        )

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "It's Rewind Time"
    app.run()
