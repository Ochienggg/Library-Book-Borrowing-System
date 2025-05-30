from lib.models.book import Book
from lib.models.patron import Patron
from lib.models.borrowrecord import BorrowRecord

def menu():
    while True:
        print("\nLibrary Management System")
        print("1. Manage Books")
        print("2. Manage Patrons")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. View Borrow Records")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            manage_books()
        elif choice == "2":
            manage_patrons()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            view_borrow_records()
        elif choice == "6":
            print("Exiting the system...")
            break
        else:
            print("Invalid option. Please try again.")

def manage_books():
    print("\nManage Books")
    print("1. Add a New Book")
    print("2. View All Books")
    print("3. Search for a Book by ID")
    print("4. Return to Main Menu")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        search_book_by_id()
    elif choice == "4":
        return
    else:
        print("Invalid choice. Try again.")

def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    book = Book(title, author)
    book.save()
    print("Book added successfully!")

def view_books():
    books = Book.get_all()
    if books:
        for book in books:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}")
    else:
        print("No books found.")

def search_book_by_id():
    try:
        book_id = int(input("Enter the Book ID: "))
        book = Book.get_by_id(book_id)
        if book:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}")
        else:
            print("Book not found.")
    except ValueError:
        print("Invalid ID format. Please enter a number.")

def manage_patrons():
    print("\nManage Patrons")
    print("1. Add a New Patron")
    print("2. View All Patrons")
    print("3. Search for a Patron by ID")
    print("4. Return to Main Menu")
    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter patron's name: ")
        patron = Patron(name)
        patron.save()
        print("Patron added successfully!")
    elif choice == "2":
        patrons = Patron.get_all()
        if patrons:
            for p in patrons:
                print(f"ID: {p.id}, Name: {p.name}")
        else:
            print("No patrons found.")
    elif choice == "3":
        try:
            patron_id = int(input("Enter Patron ID: "))
            patron = Patron.get_by_id(patron_id)
            if patron:
                print(f"ID: {patron.id}, Name: {patron.name}")
            else:
                print("Patron not found.")
        except ValueError:
            print("Invalid ID.")
    elif choice == "4":
        return
    else:
        print("Invalid option.")

def borrow_book():
    try:
        patron_id = int(input("Enter Patron ID: "))
        book_id = int(input("Enter Book ID: "))
        patron = Patron.get_by_id(patron_id)
        book = Book.get_by_id(book_id)

        if patron and book:
            if book.is_available():
                record = BorrowRecord(book_id=book.id, patron_id=patron.id)
                record.save()
                book.mark_unavailable()
                print("Book borrowed successfully!")
            else:
                print("Book is currently not available.")
        else:
            print("Invalid patron or book ID.")
    except ValueError:
        print("Invalid input. IDs must be numbers.")

def return_book():
    try:
        book_id = int(input("Enter Book ID to return: "))
        book = Book.get_by_id(book_id)
        if book and not book.is_available():
            record = BorrowRecord.get_active_by_book_id(book_id)
            if record:
                record.mark_returned()
                book.mark_available()
                print("Book returned successfully!")
            else:
                print("No active borrow record found.")
        else:
            print("Book is either invalid or already returned.")
    except ValueError:
        print("Invalid ID.")

def view_borrow_records():
    records = BorrowRecord.get_all()
    if records:
        for r in records:
            status = "Returned" if r.returned else "Borrowed"
            print(f"Record ID: {r.id}, Book ID: {r.book_id}, Patron ID: {r.patron_id}, Status: {status}")
    else:
        print("No borrow records found.")

if __name__ == "_main_":
    menu()