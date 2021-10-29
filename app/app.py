from flask import Flask

app = Flask(__name__)

@app.route("/")
def disp_home_page():
    return "hello"



if __name__ == "__main__":
    app.debug = True
    app.run()
