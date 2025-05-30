from . import CURSOR, CONN

class Book:
    def _init_(self, title, author, id=None, availability=True):
        self.id = id
        self.title = title
        self.author = author
        self.availability = availability

    @classmethod
    def create_table(cls):
        """Create the books table if it doesn't exist."""
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                availability BOOLEAN NOT NULL DEFAULT 1
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drops the books table."""
        CURSOR.execute("DROP TABLE IF EXISTS books")
        CONN.commit()

    def save(self):
        CURSOR.execute(
            "INSERT INTO books (title, author, availability) VALUES (?, ?, ?)",
            (self.title, self.author, self.availability)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid

    def delete(self):
        if self.id is None:
            raise ValueError("Cannot delete a book without an ID.")
        CURSOR.execute("DELETE FROM books WHERE id = ?", (self.id,))
        CONN.commit()

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM books")
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[0], row[3]) for row in rows]

    @classmethod
    def find_by_id(cls, book_id):
        CURSOR.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[0], row[3])
        return None

    @classmethod
    def get_by_id(cls, book_id):
        return cls.find_by_id(book_id)

    def is_available(self):
        return self.availability

    def mark_unavailable(self):
        self.availability = False
        CURSOR.execute("UPDATE books SET availability = 0 WHERE id = ?", (self.id,))
        CONN.commit()

    def mark_available(self):
        self.availability = True
        CURSOR.execute("UPDATE books SET availability = 1 WHERE id = ?", (self.id,))
        CONN.commit()