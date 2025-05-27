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
    if books
