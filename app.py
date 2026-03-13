from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["school_db"]
col = db["students"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_student():

    roll = int(request.form["roll"])
    name = request.form["name"]
    age = int(request.form["age"])
    marks = float(request.form["marks"])

    col.insert_one({
        "roll_no": roll,
        "name": name,
        "age": age,
        "marks": marks
    })

    return redirect("/students")


@app.route("/students")
def students():

    students = col.find()

    return render_template("students.html", students=students)


@app.route("/delete/<int:roll_no>")
def delete_student(roll_no):

    col.delete_one({"roll_no": roll_no})

    return redirect("/students")


if __name__ == "__main__":
    app.run(debug=True)