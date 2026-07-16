from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database Connection
def connect():
    conn = sqlite3.connect("students.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS student(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        regno TEXT,
        department TEXT,
        attendance INTEGER,
        status TEXT
    )
    """)
    return conn


# Home Page
@app.route("/")
def index():
    conn = connect()
    data = conn.execute("SELECT * FROM student").fetchall()
    conn.close()
    return render_template("index.html", students=data)


# Add Student
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        name = request.form["name"]
        regno = request.form["regno"]
        department = request.form["department"]
        attendance = int(request.form["attendance"])

        # Performance Status
        if attendance >= 90:
            status = "Excellent"
        elif attendance >= 75:
            status = "Good"
        else:
            status = "Needs Improvement"

        conn = connect()

        conn.execute("""
        INSERT INTO student(name, regno, department, attendance, status)
        VALUES (?, ?, ?, ?, ?)
        """, (name, regno, department, attendance, status))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")


# Delete Student
@app.route("/delete/<int:id>")
def delete(id):
    conn = connect()
    conn.execute("DELETE FROM student WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


# Edit Student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = connect()

    if request.method == "POST":

        name = request.form["name"]
        regno = request.form["regno"]
        department = request.form["department"]
        attendance = int(request.form["attendance"])

        if attendance >= 90:
            status = "Excellent"
        elif attendance >= 75:
            status = "Good"
        else:
            status = "Needs Improvement"

        conn.execute("""
        UPDATE student
        SET name=?, regno=?, department=?, attendance=?, status=?
        WHERE id=?
        """, (name, regno, department, attendance, status, id))

        conn.commit()
        conn.close()

        return redirect("/")

    student = conn.execute(
        "SELECT * FROM student WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit.html", student=student)


if __name__ == "__main__":
    app.run(debug=True)