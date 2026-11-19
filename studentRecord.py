
import sqlite3


# STEP 1: CONNECT TO THE DATABASE
conn = sqlite3.connect("university.db")

# Create a cursor
cursor = conn.cursor()


# STEP 2: CREATE THE STUDENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    department TEXT NOT NULL,
    level INTEGER NOT NULL,
    email TEXT UNIQUE
)
""")

conn.commit()

print("Students table created successfully!")


# STEP 3: INSERT FIVE STUDENT RECORDS
students = [
    ("John", "Ade", 20, "Computer Science", 300, "john@gmail.com"),
    ("Mary", "James", 21, "Mathematics", 300, "mary@gmail.com"),
    ("David", "Paul", 19, "Computer Science", 200, "david@gmail.com"),
    ("Sarah", "Peter", 22, "Accounting", 400, "sarah@gmail.com"),
    ("Daniel", "Joseph", 20, "Computer Science", 300, "daniel@gmail.com")
]

try:
    cursor.executemany("""
    INSERT OR IGNORE INTO students
    (first_name, last_name, age, department, level, email)
    VALUES (?, ?, ?, ?, ?, ?)
    """, students)

    conn.commit()
    print("Student records inserted successfully!")

except sqlite3.Error as e:
    print("Error inserting records:", e)


# STEP 4: RETRIEVE ALL STUDENT RECORDS
print("\nALL STUDENT RECORDS")

cursor.execute("SELECT * FROM students")

records = cursor.fetchall()

for student in records:
    print(student)


# STEP 5: RETRIEVE STUDENTS FROM A PARTICULAR DEPARTMENT
print("\nSTUDENTS IN COMPUTER SCIENCE")

cursor.execute("""
SELECT * FROM students
WHERE department = ?
""", ("Computer Science",))

department_students = cursor.fetchall()

for student in department_students:
    print(student)


# STEP 6: UPDATE A STUDENT'S LEVEL
try:
    cursor.execute("""
    UPDATE students
    SET level = ?
    WHERE email = ?
    """, (400, "john@gmail.com"))

    conn.commit()

    print("\nStudent level updated successfully!")

except sqlite3.Error as e:
    print("Error updating student:", e)


# STEP 7: DELETE A STUDENT RECORD
try:
    cursor.execute("""
    DELETE FROM students
    WHERE email = ?
    """, ("daniel@gmail.com",))

    conn.commit()

    print("Student record deleted successfully!")

except sqlite3.Error as e:
    print("Error deleting student:", e)


# STEP 8: DISPLAY THE FINAL STUDENT RECORDS
print("\nFINAL STUDENT RECORDS")

cursor.execute("SELECT * FROM students")

for student in cursor.fetchall():
    print(student)


# STEP 9: CLOSE THE DATABASE CONNECTION
conn.close()

print("\nDatabase connection closed.")
