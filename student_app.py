from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

# ---------------- CONFIG ----------------
MONGO_URI = "mongodb+srv://shailesh:Shailesh123@cluster0.am4havf.mongodb.net/school_db?retryWrites=true&w=majority"
DB_NAME = "school_db"
COLLECTION_NAME = "students"

# ---------------- CONNECT ----------------
def get_collection():
    try:
        client = MongoClient(MONGO_URI)
        # Test connection
        client.admin.command("ping")
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        # Create unique index on roll_no
        collection.create_index("roll_no", unique=True)
        return collection
    except ConnectionFailure as e:
        print("Failed to connect to MongoDB:", e)
        exit(1)


# ---------------- ADD STUDENT ----------------
def add_student(col):
    try:
        roll_no = int(input("Enter roll number: "))
        name = input("Enter name: ").strip()
        marks = float(input("Enter marks: "))

        student = {
            "roll_no": roll_no,
            "name": name,
            "marks": marks
        }

        if col.find_one({"roll_no": roll_no}):
            print("Student with this roll number already exists!")
            return

        col.insert_one(student)
        print("Student added successfully.")
    except ValueError:
        print("Invalid numeric input. Please try again.")
    except DuplicateKeyError:
        print("Duplicate roll number! Student already exists.")
    except Exception as e:
        print("Error adding student:", e)


# ---------------- VIEW STUDENT ----------------
def view_student(col):
    print("\n1. View single student by roll number")
    print("2. View all students")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        try:
            roll_no = int(input("Enter roll number: "))
        except ValueError:
            print("Invalid roll number.")
            return

        student = col.find_one({"roll_no": roll_no})
        if student:
            print("\n--- Student Details ---")
            print(f"Roll No: {student.get('roll_no')}")
            print(f"Name   : {student.get('name')}")
            print(f"Marks  : {student.get('marks')}")
        else:
            print("No student found with that roll number.")

    elif choice == "2":
        print("\n--- All Students ---")
        for student in col.find().sort("roll_no", 1):
            print(
                f"Roll No: {student.get('roll_no')}, "
                f"Name: {student.get('name')}, "
                f"Marks: {student.get('marks')}"
            )
    else:
        print("Invalid choice.")


# ---------------- UPDATE MARKS ----------------
def update_marks(col):
    try:
        roll_no = int(input("Enter roll number of student to update: "))
        new_marks = float(input("Enter new marks: "))
    except ValueError:
        print("Invalid numeric input.")
        return

    result = col.update_one({"roll_no": roll_no}, {"$set": {"marks": new_marks}})

    if result.matched_count == 0:
        print("No student found with that roll number.")
    else:
        print("Marks updated successfully.")


# ---------------- DELETE STUDENT ----------------
def delete_student(col):
    try:
        roll_no = int(input("Enter roll number of student to delete: "))
    except ValueError:
        print("Invalid roll number.")
        return

    result = col.delete_one({"roll_no": roll_no})

    if result.deleted_count == 0:
        print("No student found with that roll number.")
    else:
        print("Student record deleted successfully.")


# ---------------- MAIN MENU ----------------
def main():
    col = get_collection()
    print("Connected to MongoDB successfully.")

    while True:
        print("\n===== Student Management Menu =====")
        print("1. Add student")
        print("2. View student(s)")
        print("3. Update marks")
        print("4. Delete record")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_student(col)
        elif choice == "2":
            view_student(col)
        elif choice == "3":
            update_marks(col)
        elif choice == "4":
            delete_student(col)
        elif choice == "5":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()