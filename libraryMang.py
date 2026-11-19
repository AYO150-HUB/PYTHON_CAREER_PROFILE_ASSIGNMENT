
import sqlite3


# STEP 1: CONNECT TO THE DATABASE
conn = sqlite3.connect("library.db")

cursor = conn.cursor()


# STEP 2: CREATE THE BOOKS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publisher TEXT,
    year_published INTEGER,
    category TEXT
)
""")

conn.commit()

print("Library database created successfully!")


# STEP 3: FUNCTION TO REGISTER A BOOK
def register_book():

    print("\nREGISTER A NEW BOOK")

    title = input("Enter book title: ")
    author = input("Enter author name: ")
    publisher = input("Enter publisher: ")

    try:
        year = int(input("Enter year published: "))

        category = input("Enter book category: ")

        cursor.execute("""
        INSERT INTO books
        (title, author, publisher, year_published, category)
        VALUES (?, ?, ?, ?, ?)
        """, (title, author, publisher, year, category))

        conn.commit()

        print("Book registered successfully!")

    except ValueError:
        print("Error: Year published must be a number.")

    except sqlite3.Error as e:
        print("Database error:", e)


# STEP 4: FUNCTION TO RETRIEVE ALL BOOKS
def retrieve_books():

    print("\nALL REGISTERED BOOKS")

    try:
        cursor.execute("SELECT * FROM books")

        books = cursor.fetchall()

        if books:
            for book in books:
                print(book)

        else:
            print("No books found.")

    except sqlite3.Error as e:
        print("Error retrieving books:", e)


# STEP 5: FUNCTION TO SEARCH FOR A BOOK
def search_book():

    print("\nSEARCH FOR A BOOK")

    title = input("Enter book title to search: ")

    try:
        cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ?
        """, ('%' + title + '%',))

        books = cursor.fetchall()

        if books:
            print("\nSEARCH RESULTS")

            for book in books:
                print(book)

        else:
            print("Book not found.")

    except sqlite3.Error as e:
        print("Search error:", e)


# STEP 6: FUNCTION TO MODIFY BOOK INFORMATION
def modify_book():

    print("\nMODIFY BOOK INFORMATION")

    try:
        book_id = int(input("Enter the book ID to modify: "))

        title = input("Enter new book title: ")
        author = input("Enter new author: ")
        publisher = input("Enter new publisher: ")

        year = int(input("Enter new publication year: "))

        category = input("Enter new category: ")

        cursor.execute("""
        UPDATE books

        SET title = ?,
            author = ?,
            publisher = ?,
            year_published = ?,
            category = ?

        WHERE book_id = ?
        """, (title, author, publisher, year, category, book_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Book information updated successfully!")

        else:
            print("No book found with that ID.")

    except ValueError:
        print("Error: Enter a valid number for ID and year.")

    except sqlite3.Error as e:
        print("Modification error:", e)


# STEP 7: FUNCTION TO DELETE A BOOK
def delete_book():

    print("\nDELETE A BOOK")

    try:
        book_id = int(input("Enter the book ID to delete: "))

        cursor.execute("""
        DELETE FROM books
        WHERE book_id = ?
        """, (book_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Book deleted successfully!")

        else:
            print("No book found with that ID.")

    except ValueError:
        print("Error: Book ID must be a number.")

    except sqlite3.Error as e:
        print("Deletion error:", e)


# STEP 8: CREATE THE MAIN MENU
def main():

    while True:

        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")

        print("1. Register a Book")
        print("2. Retrieve All Books")
        print("3. Search for a Book")
        print("4. Modify Book Information")
        print("5. Delete a Book")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            register_book()

        elif choice == "2":
            retrieve_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            modify_book()

        elif choice == "5":
            delete_book()

        elif choice == "6":
            print("Exiting Library Management System.")
            break

        else:
            print("Invalid choice. Please select 1-6.")


# STEP 9: RUN THE PROGRAM
try:
    main()

finally:
    conn.close()
    print("Database connection closed.")
