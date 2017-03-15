from flask import Flask, request, render_template, redirect
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

    github = request.args.get('github', 'jhacks')
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

    sql = """INSERT INTO students (first_name, last_name, github)
                VALUES (:first_name, :last_name, :github)
          """
    db.session.execute(sql, {'first_name': first_name,
                             'last_name': last_name,
                             'github': github})
    db.session.commit()

    print "New student generated."
    return redirect("/student-added-success")


@app.route("/student-form")
def new_student():
    """rendering the form to input data to student"""

    return render_template("student_add.html")


@app.route("/student-added-success")
def new_student_success():
    """when successfully added student, showing what is added"""

    github = request.args.get('github')
    return render_template("student_added.html", github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
