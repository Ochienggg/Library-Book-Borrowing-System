from lib.models.book import Book
from lib.models.patron import Patron
from lib.models.borrowrecord import BorrowRecord
from datetime import date

def get_book_details():
    """Helper function to get book details from the user."""
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    return title, author

def get_patron_details():
    """Helper function to get patron details from the user."""
    name = input("Enter patron's name: ")
    email = input("Enter patron's email: ")
    phone = input("Enter patron's phone number: ")
    return name, email, phone

def add_new_book():
    """Adds a new book to the system."""
    title, author = get_book_details()
    book = Book(title, author)
    book.save()
    print(f"Book '{title}' by {author} has been added to the library.")

def list_all_books():
    """Lists all books in the system."""
    books = Book.get_all()
    if books:
        print("\nList of Books:")
        for book in books:
            availability = "Available" if book.availability else "Borrowed"
            print(f"ID: {book.id} | Title: {book.title} | Author: {book.author} | Status: {availability}")
    else:
        print("No books found in the library.")

def search_book_by_id():
    """Searches for a book by ID."""
    book_id = input("Enter book ID: ")
    book = Book.find_by_id(book_id)
    if book:
        availability = "Available" if book.availability else "Borrowed"
        print(f"Book ID: {book.id} | Title: {book.title} | Author: {book.author} | Status: {availability}")
    else:
        print(f"No book found with ID {book_id}.")

def add_new_patron():
    """Adds a new patron to the system."""
    name, email, phone = get_patron_details()
    patron = Patron(name, email, phone)
    patron.save()
    print(f"Patron {name} has been added to the system.")

def list_all_patrons():
    """Lists all patrons in the system."""
    patrons = Patron.get_all()
    if patrons:
        print("\nList of Patrons:")
        for patron in patrons:
            print(f"ID: {patron.id} | Name: {patron.name} | Email: {patron.email} | Phone: {patron.phone}")
    else:
        print("No patrons found in the system.")

def borrow_book():
    """Borrow a book for a patron."""
    book_id = input("Enter book ID to borrow: ")
    book = Book.find_by_id(book_id)

    if not book:
        print(f"Book with ID {book_id} not found.")
        return

    if not book.availability:
        print(f"Book '{book.title}' is already borrowed.")
        return

    patron_id = input("Enter patron ID: ")
    patron = Patron.find_by_id(patron_id)

    if not patron:
        print(f"Patron with ID {patron_id} not found.")
        return

    borrow_record = BorrowRecord(patron_id, book_id)
    borrow_record.save()
    book.mark_as_borrowed()  # Mark the book as borrowed
    print(f"Book '{book.title}' has been borrowed by {patron.name}.")

def return_book():
    """Return a borrowed book."""
    borrow_id = input("Enter borrow record ID to return: ")
    borrow_record = BorrowRecord.find_by_id(borrow_id)

    if not borrow_record:
        print(f"Borrow record with ID {borrow_id} not found.")
        return

    book = Book.find_by_id(borrow_record.book_id)
    patron = Patron.find_by_id(borrow_record.patron_id)

    if not book or not patron:
        print("Associated book or patron not found.")
        return

    borrow_record.mark_returned()
    book.mark_as_returned()  # Mark the book as available
    print(f"Book '{book.title}' has been returned by {patron.name}.")

def list_borrowed_books():
    """List borrowed books with due dates."""
    borrow_records = BorrowRecord.get_all()
    if borrow_records:
        print("\nList of Borrowed Books:")
        for record in borrow_records:
            book = Book.find_by_id(record.book_id)
            patron = Patron.find_by_id(record.patron_id)
            status = "Returned" if record.return_date else "Borrowed (Not Returned)"
            print(f"Record ID: {record.id} | Book: {book.title} | Patron: {patron.name} | Status: {status}")
    else:
        print("No borrow records found.")

def overdue_books():
    """List all overdue books."""
    today = date.today().isoformat()
    borrow_records = BorrowRecord.get_all()
    overdue_records = [record for record in borrow_records if record.return_date is None and record.borrow_date < today]

    if overdue_records:
        print("\nOverdue Books:")
        for record in overdue_records:
            book = Book.find_by_id(record.book_id)
            patron = Patron.find_by_id(record.patron_id)
            print(f"Record ID: {record.id} | Book: {book.title} | Patron: {patron.name} | Due Date: {record.borrow_date}")
    else:
        print("No overdue books found.")
