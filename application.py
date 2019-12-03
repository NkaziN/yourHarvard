import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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
db = SQL("sqlite:///yourharvardv1.db")

# # Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show current plan of study"""
    # course = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    # if not course:
    #     return apology("no stock with such symbol", 400)

    # stocks = db.execute(
    #     "SELECT symbol, SUM(shares) FROM transactions WHERE user_id = :user_id GROUP BY lower(symbol) HAVING SUM(shares) != 0", user_id=session["user_id"])
    # # get current amount of cash
    # # cash = cash[0]['cash']

    # # lookup for each stock to get the price of each stock currently - this code works
    # for stock in stocks:
    #     quote = lookup(stock["symbol"])
    #     stock['symbol'] = quote['symbol']
    #     stock["name"] = quote['name']
    #     stock["price"] = float(quote['price'])
    #     stock['shares'] = int(stock['SUM(shares)'])
    #     stock['total'] = stock['SUM(shares)'] * quote['price']
    #     grandtot = grandtot + stock['total']  # keep updating the grand total
    # # render template with the courses selected, recall to give context to the page
    return render_template("index.html")


@app.route("/concentration", methods=["GET", "POST"])
@login_required
def concentration():
    """Get the courses for a concentration"""
    if request.method == "POST":
        concentrationname = request.form.get("ConcentrationName")
        if not concentrationname:
            return apology("concentration name is invalid", 400)

        # update the concentration that the user chose in the sql table- MODIFY
        # db.execute("UPDATE users SET cash = cash - :moneyreq WHERE id = :user_id", moneyreq=moneyreq, user_id=session['user_id'])
        return render_template("schedule.html", concentrationname=concentrationname)
    else:
        # modify this line of code to get the names of concentrations
        names = db.execute(
            "SELECT name FROM concentrations")
        concentrations = [name["name"] for name in names]

        return render_template("concentration.html", concentrations=concentrations)

@app.route("/schedule")
@login_required
def schedule():
    # get concentration related info
    concentrationname = request.form.get("ConcentrationName")
    courses = db.execute("SELECT * FROM concentrations JOIN requirements ON concentrations.id = requirements.conc_id JOIN courses ON requirements.course_code = courses.code WHERE concentrations.name = 'Anthropology';")

    # remember to provide context for returning pages
    return render_template("schedule.html", courses = courses, concentrationname=concentrationname)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # if no username is provided
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # if no password is provided
        if not request.form.get("password"):
            return apology("must provide password", 400)
        # if passwords don't match up
        if request.form.get("password") != request.form.get("passwordagain"):
            return apology("passwords don't match up", 400)
        # insert user into table
        username = request.form.get("username")

        password = generate_password_hash(request.form.get("password"))
        # password = hash(request.form.get("password"))
        id = db.execute("INSERT INTO users (username, hash) VALUES (:username,:password)",
                        username=username, password=password)
        # if username is already taken
        if not id:
            return apology("username already taken", 400)
            # alert("username not available")
        # return to homepage for user after register

        return redirect("/")
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
