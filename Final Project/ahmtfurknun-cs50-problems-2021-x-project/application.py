import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///data.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]
        tasks = db.execute("SELECT key, task FROM list WHERE username = :username", username=username)
        if len(tasks) != 0:
            bo = True
            return render_template("index.html", tasks=tasks, bo=bo)
        else:
            bo = False
            return render_template("index.html", tasks=tasks, bo=bo)

    else:
        keys = request.form.getlist("task_keys")
        for i in keys:
            db.execute("INSERT INTO done (username, task, date) VALUES (:username, :task, :date)",
                   username=db.execute("SELECT username FROM users WHERE id = :uid",
                                       uid=int(session['user_id']))[0]["username"],
                   task=db.execute("SELECT task FROM list WHERE key = :key", key = i)[0]["task"],
                   date=datetime.datetime.now().strftime("%x"))
            db.execute("DELETE FROM list WHERE key = :key", key = i)
            

        return redirect("/")


@app.route("/add", methods=["POST"])
@login_required
def add():
    task = request.form.get("task")
   
    if not len(task) > 0:
        return apology("invalid input", 400)

    db.execute("INSERT INTO list (username, task) VALUES (:username, :task)",
               username=db.execute("SELECT username FROM users WHERE id = :uid",
                                   uid=int(session['user_id']))[0]["username"],
               task=request.form.get('task'))

    return redirect("/")


@app.route("/done", methods=["GET", "POST"])
@login_required
def done():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]
        tasks = db.execute("SELECT key, task, date FROM done WHERE username = :username", username=username)
        if len(tasks) != 0:
            bo = True
            return render_template("done.html", tasks=tasks, bo=bo)
        else:
            bo = False
            return render_template("done.html", tasks=tasks, bo=bo)
        
        
    else:
        keys = request.form.getlist("task_keys")
        for i in keys:
            db.execute("DELETE FROM done WHERE key = :key", key = i)

        return redirect("/done")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def sell():
    """remove"""
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]
    if request.method == "GET":
        tasks = db.execute("SELECT key, task FROM list WHERE username = :username", username=username)
        if len(tasks) != 0:
            bo = True
            return render_template("remove.html", tasks=tasks, bo=bo)
        else:
            bo = False
            return render_template("remove.html", tasks=tasks, bo=bo)

    else:
        keys = request.form.getlist("task_keys")
        for i in keys:
            db.execute("DELETE FROM list WHERE key = :key", key = i)

        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        usernames = db.execute("SELECT username FROM users")
        for i in range(len(usernames)):
            if request.form.get("username") == usernames[i]["username"]:
                return apology("username already exists", 400)

        if not request.form.get("username"):
            return apology("must provide username", 400)
# Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password again", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords are not same", 400)

        x = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get(
            "password")))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)