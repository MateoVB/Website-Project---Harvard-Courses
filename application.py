import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)    CHANGE THIS IN CASE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///courses.db")

@app.route("/CS20")
def CS20():
    return render_template("CS20.html")

@app.route("/CS51")
def CS51():
    return render_template("CS51.html")

@app.route("/CS61")
def CS61():
    return render_template("CS61.html")

@app.route("/CS100")
def CS100():
    return render_template("CS100.html")

@app.route("/CS105")
def CS105():
    return render_template("CS105.html")

@app.route("/CS109A")
def CS109A():
    return render_template("CS109A.html")

@app.route("/CS109B")
def CS109B():
    return render_template("CS109B.html")

@app.route("/CS121")
def CS121():
    return render_template("CS121.html")

@app.route("/CS124")
def CS124():
    return render_template("CS124.html")

@app.route("/CS134")
def CS134():
    return render_template("CS134.html")

@app.route("/CS136")
def CS136():
    return render_template("CS136.html")

@app.route("/CS141")
def CS141():
    return render_template("CS141.html")

@app.route("/CS143")
def CS143():
    return render_template("CS143.html")

@app.route("/CS152")
def CS152():
    return render_template("CS152.html")

@app.route("/CS153")
def CS153():
    return render_template("CS153.html")

@app.route("/CS161")
def CS161():
    return render_template("CS161.html")

@app.route("/CS165")
def CS165():
    return render_template("CS165.html")

@app.route("/CS171")
def CS171():
    return render_template("CS171.html")

@app.route("/CS175")
def CS175():
    return render_template("CS175.html")

@app.route("/CS179")
def CS179():
    return render_template("CS179.html")

@app.route("/CS181")
def CS181():
    return render_template("CS181.html")

@app.route("/CS182")
def CS182():
    return render_template("CS182.html")

@app.route("/CS189")
def CS189():
    return render_template("CS189.html")

@app.route("/CS191")
def CS191():
    return render_template("CS191.html")

@app.route("/")
def index():
    """Show portfolio of stocks"""

    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        workload = request.form.get("workload")
        if not workload:
            workload = 100
        course = request.form.get("course")
        if not course:
            course = 0
        instructor = request.form.get("instructor")
        if not instructor:
            instructor = 0
        recommended = request.form.get("recommended")
        if not recommended:
            recommended = 0
        semester = request.form.get("semester")
        if semester == "fall":
            rows = db.execute("SELECT * FROM fall WHERE  Workload <= ? AND ? <= CScore AND ? <= Iscore AND ? <= Recommend",
            workload, course, instructor, recommended)
        elif semester == "spring":
            rows = db.execute("SELECT * FROM spring WHERE  Workload <= ? AND ? <= CScore AND ? <= Iscore AND ? <= Recommend",
            workload, course, instructor, recommended)
        else:
            rows = db.execute("SELECT * FROM fall WHERE  Workload <= ? AND ? <= CScore AND ? <= Iscore AND ? <= Recommend UNION SELECT * FROM spring WHERE  Workload <= ? AND ? <= CScore AND ? <= Iscore AND ? <= Recommend",
            workload, course, instructor, recommended, workload, course, instructor, recommended)
        if not rows:
            return render_template("error.html", num = 5)
        else:
            return render_template("searched.html", rows=rows)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/all", methods=["GET", "POST"])
def all():
    rows = db.execute("SELECT * FROM fall UNION SELECT * FROM spring ORDER BY Title ASC")
    return render_template("all.html", rows=rows)

@app.route("/compare", methods=["GET", "POST"])
def compare():
    if request.method == "GET":
        data = db.execute("SELECT * FROM spring")
        return render_template("compare.html", data = data)
    else:
        course1name = request.form.get("course1")
        course2name = request.form.get("course2")
        if not course1name:
            return render_template("error.html", num = 1)
        if not course2name:
            return render_template("error.html", num = 2)
        course1 = int(request.form.get("course1"))
        course2 = int(request.form.get("course2"))
        rows = db.execute("SELECT ID FROM fall UNION SELECT ID FROM spring")
        ifcourse1 = 0
        ifcourse2 = 0
        for x in rows:
            if x["ID"] == course1:
                ifcourse1 = 1
        for x in rows:
            if x["ID"] == course2:
                ifcourse2 = 1
        if ifcourse1 == 0:
            return render_template("error.html", num = 3)
        if ifcourse2 == 0:
            return render_template("error.html", num = 4)
        course1info = db.execute("SELECT * FROM fall UNION SELECT * FROM spring WHERE ID = ?", course1)
        course2info = db.execute("SELECT * FROM fall UNION SELECT * FROM spring WHERE ID = ?", course2)
        return render_template("compared.html", course1info = course1info, course2info = course2info, course1 = course1, course2 = course2)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return "Sorry there was an error"

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
