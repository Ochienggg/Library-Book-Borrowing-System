from models.__init__ import CURSOR, CONN
from datetime import date

class BorrowRecord:
    def __init__(self, patron_id, book_id, borrow_date=None, return_date=None, id=None):
        self.id = id
        self.patron_id = patron_id
        self.book_id = book_id
        self.borrow_date = borrow_date or date.today().isoformat()
        self.return_date = return_date

    @classmethod
    def create_table(cls):
        """Create the borrow_records table if it doesn't exist."""
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS borrow_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patron_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY(patron_id) REFERENCES patrons(id),
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drops the borrow_records table."""
    CURSOR.execute("DROP TABLE IF EXISTS borrow_records")
    CONN.commit()


    def save(self):
        CURSOR.execute(
            "INSERT INTO borrow_records (patron_id, book_id, borrow_date, return_date) VALUES (?, ?, ?, ?)",
            (self.patron_id, self.book_id, self.borrow_date, self.return_date)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid

    def delete(self):
        if self.id is None:
            raise ValueError("Cannot delete a borrow record without an ID.")
        CURSOR.execute("DELETE FROM borrow_records WHERE id = ?", (self.id,))
        CONN.commit()

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM borrow_records")
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[4], id=row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, record_id):
        CURSOR.execute("SELECT * FROM borrow_records WHERE id = ?", (record_id,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[4], id=row[0])
        return None

    def mark_returned(self):
        self.return_date = date.today().isoformat()
        CURSOR.execute("UPDATE borrow_records SET return_date = ? WHERE id = ?", (self.return_date, self.id))
        CONN.commit()

