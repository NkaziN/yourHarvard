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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///yourharvard.db")


@app.route("/")
@login_required
def index():
    """Show current plan of study"""

    # render template with the courses selected, recall to give context to the page
    return render_template("index.html")


@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    """Get the courses for a concentration"""
    if request.method == "POST":
        # get the names of concentrations
        names = db.execute(
            "SELECT name FROM concentrations")
        concentrations = [name["name"] for name in names]
        concentrationname = request.form.get("ConcentrationName")
        # if an invalid concentration name is entered
        if not concentrationname:
            return apology("concentration name is invalid", 400)
        numbers = db.execute("SELECT required FROM concentrations WHERE name = ?;", concentrationname)
        # Avoid error if no courses are retrieve
        if numbers:
            numreq = numbers[0]["required"]
        else:
            numreq = ""
        courses = db.execute("SELECT * FROM concentrations JOIN requirements ON concentrations.id = requirements.conc_id JOIN courses ON requirements.course_code = courses.code WHERE concentrations.name = ?;", concentrationname)
        exceptions = db.execute("SELECT * FROM requirements WHERE course_code LIKE 'Choose%' AND requirements.conc_id IN (SELECT id FROM concentrations WHERE name = ?);", concentrationname)
        # render schedule.html with the context and all the courses for the given concentration
        return render_template("schedule.html", courses = courses, concentrationname=concentrationname, numreq = numreq, concentrations=concentrations, exceptions=exceptions)
    else:
        # get the names of concentrations
        names = db.execute(
            "SELECT name FROM concentrations")
        concentrations = [name["name"] for name in names]
        # render schedule.html with the context
        return render_template("schedule.html", concentrations=concentrations)

@app.route("/courseexplorer", methods=["GET", "POST"])
@login_required
def courseexplorer():
    if request.method == "POST":
         # get the names of concentrations and place it in the dropdown menu
        names = db.execute(
                "SELECT name FROM concentrations")
        concentrations = [name["name"] for name in names]

        # get the selected concentration
        concentrationname = request.form.get("ConcentrationName")
        if not concentrationname:
            return apology("concentration name is invalid", 400)

        # get all the filtered courses for a concentration and display them in blocks, need to modify the table this is selecting from
        courses = db.execute("SELECT DISTINCT * FROM concentrations JOIN explorer ON concentrations.id = explorer.conc_id JOIN courses ON explorer.course_code = courses.code WHERE explorer.conc_id IN (SELECT id FROM concentrations WHERE name = ?);", concentrationname)
        exceptions = db.execute("SELECT DISTINCT * FROM explorer WHERE explorer.course_code LIKE 'Any%' AND explorer.conc_id IN (SELECT id FROM concentrations WHERE name = ?);", concentrationname)
        numCourses = len(courses)
        return render_template("courseexplorer.html", courses = courses, concentrationname=concentrationname, concentrations=concentrations, exceptions=exceptions, numCourses=numCourses)
    else:
        # get the names of concentrations and place it in the dropdown menu
        names = db.execute(
                "SELECT name FROM concentrations")
        concentrations = [name["name"] for name in names]

        # provide context for returning pages
        return render_template("courseexplorer.html", concentrations=concentrations)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html",username="Missing!",password="Password")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html",username="Username",password="Missing!")

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
        return render_template("login.html",username="Username",password="Password")


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
            return render_template("register.html",username="Missing!",password="Password", passwordagain = "Password(again)")
        # if no password is provided
        if not request.form.get("password"):
            return render_template("register.html",username="Username",password="Missing!", passwordagain = "Password(again)")
        # if passwords don't match up
        if request.form.get("password") != request.form.get("passwordagain"):
            return render_template("register.html",username="Username",password="Password", passwordagain = "Retype!")
        # insert user into table
        username = request.form.get("username")

        password = generate_password_hash(request.form.get("password"))
        # password = hash(request.form.get("password"))
        id = db.execute("INSERT INTO users (username, hash) VALUES (:username,:password)",
                        username=username, password=password)
        # if username is already taken
        if not id:
            return render_template("register.html",username="Taken!",password="Password", passwordagain = "Password(again)")
            # alert("username not available")

        # return to homepage for user after register
        return redirect("/")
    else:
        return render_template("register.html",username="Username",password="Password", passwordagain = "Password(again)")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
