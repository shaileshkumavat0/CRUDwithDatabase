from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://shailesh:Shailesh123@cluster0.am4havf.mongodb.net/school_db?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client["school_db"]

col = db["students"]


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Add Student
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


# View Students
@app.route("/students")
def view_students():

    students = col.find().sort("roll_no", 1)

    return render_template("students.html", students=students)


# Delete Student
@app.route("/delete/<int:roll_no>")
def delete_student(roll_no):

    col.delete_one({"roll_no": roll_no})

    return redirect("/students")

@app.route("/edit/<int:roll_no>")
def edit_student(roll_no):

    student = col.find_one({"roll_no": roll_no})

    return render_template("edit.html", student=student)


@app.route("/update/<int:roll_no>", methods=["POST"])
def update_student(roll_no):

    name = request.form["name"]
    age = int(request.form["age"])
    marks = float(request.form["marks"])

    col.update_one(
        {"roll_no": roll_no},
        {"$set": {
            "name": name,
            "age": age,
            "marks": marks
        }}
    )

    return redirect("/students")

if __name__ == "__main__":
    app.run(debug=True)