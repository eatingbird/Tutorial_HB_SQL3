from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import hackbright

db = SQLAlchemy()


def connect_to_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

app = Flask(__name__)

connect_to_db(app)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    print "New student generated."

    # # Solution1
    # return render_template("student_added.html", github=github)

    # Solution 2 URL FOR
    print url_for('new_student_success', github=github)
    return redirect(url_for('new_student_success', github=github))


@app.route("/student-form")
def new_student():
    """rendering the form to input data to student"""

    return render_template("student_add.html")


@app.route("/student-added-success")
def new_student_success():
    """when successfully added student, showing what is added"""

    github = request.args.get('github')
    return render_template("student_added.html", github=github)

"""
# Solution 3
@add.route("/student/<github>")
def show_student(github):
    return render_template(github=github)

/student-serach-process
    #GET
    will change into 
    return redirect student URL FOR(show_student, github=github)
    because you are passing github

/student-add-process
    #POST
    #process add form 
    return redirect to student (URL FOR)
    because you are passing github

"""    


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
