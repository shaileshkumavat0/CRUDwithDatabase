from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Create Flask app
app = Flask(__name__)

# MongoDB Atlas URI
MONGO_URI = "mongodb+srv://shailesh:Shailesh123@cluster0.am4havf.mongodb.net/school_db?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["school_db"]
col = db["students"]

# Create unique index for roll number
col.create_index("roll_no", unique=True)


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADD STUDENT ----------------
@app.route("/add", methods=["POST"])
def add_student():

    roll = int(request.form["roll"])
    name = request.form["name"]
    marks = float(request.form["marks"])
    age = int(request.form["age"])
    course = request.form["course"]

    # Check duplicate roll number
    if col.find_one({"roll_no": roll}):
        return "Student with this roll number already exists!"

    try:
        col.insert_one({
            "roll_no": roll,
            "name": name,
            "marks": marks,
            "age": age,
            "course": course
        })
    except DuplicateKeyError:
        return "Duplicate roll number!"

    return redirect("/students")


# ---------------- VIEW STUDENTS ----------------
@app.route("/students")
def view_students():

    students = col.find().sort("roll_no", 1)

    return render_template("students.html", students=students)


# ---------------- DELETE STUDENT ----------------
@app.route("/delete/<int:roll_no>")
def delete_student(roll_no):

    col.delete_one({"roll_no": roll_no})

    return redirect("/students")


# ---------------- EDIT PAGE ----------------
@app.route("/edit/<int:roll_no>")
def edit_student(roll_no):

    student = col.find_one({"roll_no": roll_no})

    return render_template("edit.html", student=student)


# ---------------- UPDATE STUDENT ----------------
@app.route("/update/<int:roll_no>", methods=["POST"])
def update_student(roll_no):

    name = request.form["name"]
    marks = float(request.form["marks"])
    age = int(request.form["age"])
    course = request.form["course"]

    col.update_one(
    {"roll_no": roll_no},
    {"$set": {
        "name": name,
        "marks": marks,
        "course": course
    }}
)

    return redirect("/students")


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)