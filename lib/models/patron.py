from . import CURSOR, CONN

class Patron:
    def __init__(self, name, email, phone=None, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

    @classmethod
    def create_table(cls):
        """Create the patrons table if it doesn't exist."""
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS patrons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the patrons table."""
        CURSOR.execute("DROP TABLE IF EXISTS patrons")
        CONN.commit()

    def save(self):
        """Save the Patron to the database."""
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO patrons (name, email, phone) VALUES (?, ?, ?)",
                (self.name, self.email, self.phone)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute(
                "UPDATE patrons SET name = ?, email = ?, phone = ? WHERE id = ?",
                (self.name, self.email, self.phone, self.id)
            )
            CONN.commit()

    def delete(self):
        """Delete the Patron from the database."""
        if self.id is None:
            raise ValueError("Cannot delete a patron without an ID.")
        CURSOR.execute("DELETE FROM patrons WHERE id = ?", (self.id,))
        CONN.commit()

    @classmethod
    def get_all(cls):
        """Return a list of all patrons."""
        CURSOR.execute("SELECT * FROM patrons")
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], id=row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, patron_id):
        """Find a patron by ID."""
        CURSOR.execute("SELECT * FROM patrons WHERE id = ?", (patron_id,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], id=row[0])
        return None

    @classmethod
    def get_by_id(cls, patron_id):
        """Alias for find_by_id."""
        return cls.find_by_id(patron_id)

    def __str__(self):
        return f"{self.name} (Email: {self.email}, Phone: {self.phone})"
