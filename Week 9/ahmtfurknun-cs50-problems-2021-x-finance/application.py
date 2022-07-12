import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]
    stocks = db.execute("SELECT symbol, shares FROM portfolio WHERE username = :username", username=username)
    lst = list()
    for stock in stocks:
        symbol = str(stock["symbol"])
        shares = int(stock["shares"])
        name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]
        total = shares * price
        stock["name"] = name
        stock["price"] = usd(price)
        stock["total"] = usd(total)
        lst.append(float(total))

    available = db.execute("SELECT cash FROM users WHERE username = :username", username=username)[0]["cash"]
    totalcash = sum(lst) + available

    return render_template("index.html", stocks=stocks, available=usd(available), totalcash=usd(totalcash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        look = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")

        if look == None:
            return apology("invalid symbol", 400)

        elif not shares.isdigit() or int(shares) < 1:
            return apology("share must be at least 1", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=int(session['user_id']))
        value = look["price"] * int(shares)

        if int(cash[0]["cash"]) < value:
            return apology("not enough cash", 400)

        else:
            db.execute("UPDATE users SET cash = cash - :value WHERE id = :uid", value=value, uid=int(session['user_id']))
            db.execute("INSERT INTO history (username, operation, symbol, price, shares) VALUES (:username, 'BUY', :symbol, :price, :shares)",
                       username=db.execute("SELECT username FROM users WHERE id = :uid",
                                           uid=int(session['user_id']))[0]["username"],
                       symbol=look['symbol'], price=look['price'], shares=request.form.get('shares'))

            db.execute("INSERT INTO portfolio (username, symbol, shares) VALUES (:username, :symbol, :shares)",
                       username=db.execute("SELECT username FROM users WHERE id = :uid",
                                           uid=int(session['user_id']))[0]["username"],
                       symbol=look['symbol'], shares=request.form.get('shares'))

            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]
    stocks = db.execute(
        "SELECT operation, symbol, price, date, time, shares FROM history WHERE username = :username", username=username)
    for stock in stocks:
        symbol = str(stock["symbol"])
        name = lookup(symbol)["name"]
        stock["name"] = name
    return render_template("history.html", stocks=stocks)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        look = lookup(request.form.get("symbol"))
        if look == None:
            return apology("invalid symbol", 400)

        else:
            return render_template("quoted.html", name=look["name"], symbol=look["symbol"], price=usd(look["price"]))


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]
    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM portfolio WHERE username = :username", username=username)
        return render_template("sell.html", symbols=symbols)

    else:
        look = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")
        user_shares = db.execute("SELECT shares FROM portfolio WHERE username = :username and symbol = :symbol",
                                 username=username, symbol=str(request.form.get("symbol")))[0]["shares"]
        value = look["price"] * int(shares)
        if not request.form.get("symbol") or look == None:
            return apology("invalid symbol", 400)

        elif not shares or not shares.isdigit() or int(shares) < 1 or int(shares) > int(user_shares):
            return apology("share number is invalid", 400)

        else:
            db.execute("UPDATE users SET cash = cash + :value WHERE id = :uid", value=value, uid=int(session['user_id']))
            db.execute("INSERT INTO history (username, operation, symbol, price, shares) VALUES (:username, 'SELL', :symbol, :price, :shares)",
                       username=username, symbol=look['symbol'], price=look['price'], shares=request.form.get('shares'))
            if int(user_shares) == int(shares):
                db.execute("DELETE FROM portfolio WHERE username = :username and symbol = :symbol",
                           username=username, symbol=str(request.form.get("symbol")))

            elif int(user_shares) > int(shares):
                db.execute("UPDATE portfolio SET shares = :shares WHERE username = :username and symbol = :symbol",
                           shares=shares, username=username, symbol=request.form.get("symbol"))

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
