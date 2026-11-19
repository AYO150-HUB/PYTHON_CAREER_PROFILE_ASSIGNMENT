
import sqlite3


# STEP 1: CONNECT TO THE DATABASE
conn = sqlite3.connect("course_registration.db")

# Enable foreign key constraints
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()


# STEP 2: CREATE THE STUDENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE
)
""")


# STEP 3: CREATE THE COURSES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    course_code TEXT UNIQUE NOT NULL,
    credit_unit INTEGER
)
""")


# STEP 4: CREATE THE ENROLLMENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,

    FOREIGN KEY (student_id)
    REFERENCES students(student_id),

    FOREIGN KEY (course_id)
    REFERENCES courses(course_id),

    UNIQUE(student_id, course_id)
)
""")

conn.commit()

print("Database tables created successfully!")


# STEP 5: FUNCTION TO REGISTER STUDENTS
def register_student(first_name, last_name, email):

    try:
        cursor.execute("""
        INSERT INTO students (first_name, last_name, email)
        VALUES (?, ?, ?)
        """, (first_name, last_name, email))

        conn.commit()

        print("Student registered successfully!")

    except sqlite3.IntegrityError as e:
        print("Student registration error:", e)


# STEP 6: FUNCTION TO REGISTER COURSES
def register_course(course_name, course_code, credit_unit):

    try:
        cursor.execute("""
        INSERT INTO courses
        (course_name, course_code, credit_unit)
        VALUES (?, ?, ?)
        """, (course_name, course_code, credit_unit))

        conn.commit()

        print("Course registered successfully!")

    except sqlite3.IntegrityError as e:
        print("Course registration error:", e)


# STEP 7: FUNCTION TO ENROLL A STUDENT IN A COURSE
def enroll_student(student_id, course_id):

    try:
        cursor.execute("""
        INSERT INTO enrollments (student_id, course_id)
        VALUES (?, ?)
        """, (student_id, course_id))

        conn.commit()

        print("Student enrolled successfully!")

    except sqlite3.IntegrityError as e:
        print("Enrollment error:", e)


# STEP 8: RETRIEVE ALL STUDENTS
def retrieve_students():

    print("\nREGISTERED STUDENTS")

    cursor.execute("SELECT * FROM students")

    for student in cursor.fetchall():
        print(student)


# STEP 9: RETRIEVE ALL COURSES
def retrieve_courses():

    print("\nREGISTERED COURSES")

    cursor.execute("SELECT * FROM courses")

    for course in cursor.fetchall():
        print(course)


# STEP 10: DISPLAY STUDENTS AND THEIR COURSES
def retrieve_student_courses():

    print("\nSTUDENT COURSE REGISTRATION DETAILS")

    cursor.execute("""
    SELECT
        students.first_name,
        students.last_name,
        courses.course_name,
        courses.course_code

    FROM enrollments

    JOIN students
    ON enrollments.student_id = students.student_id

    JOIN courses
    ON enrollments.course_id = courses.course_id
    """)

    records = cursor.fetchall()

    for record in records:
        print(record)


# STEP 11: REGISTER SAMPLE STUDENTS
register_student("John", "Ade", "john@gmail.com")
register_student("Mary", "James", "mary@gmail.com")


# STEP 12: REGISTER SAMPLE COURSES
register_course("Python Programming", "CSC334", 3)
register_course("Database Management", "CSC312", 3)
register_course("Data Structures", "CSC311", 3)


# STEP 13: DISPLAY STUDENTS AND COURSES
retrieve_students()
retrieve_courses()


# STEP 14: ENROLL STUDENTS IN COURSES
enroll_student(1, 1)
enroll_student(1, 2)
enroll_student(2, 1)
enroll_student(2, 3)


# STEP 15: DISPLAY THE RELATIONSHIP
retrieve_student_courses()


# STEP 16: CLOSE DATABASE CONNECTION
conn.close()

print("\nDatabase connection closed.")
