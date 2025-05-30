from . import CURSOR, CONN

class Patron:
    def _init_(self, name, email=None, phone=None, id=None):
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
        """Drops the patrons table."""
        CURSOR.execute("DROP TABLE IF EXISTS patrons")
        CONN.commit()

    def save(self):
        CURSOR.execute(
            "INSERT INTO patrons (name, email, phone) VALUES (?, ?, ?)",
            (self.name, self.email, self.phone)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid

    def delete(self):
        if self.id is None:
            raise ValueError("Cannot delete a patron without an ID.")
        CURSOR.execute("DELETE FROM patrons WHERE id = ?", (self.id,))
        CONN.commit()

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM patrons")
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[0]) for row in rows]

    @classmethod
    def find_by_id(cls, patron_id):
        CURSOR.execute("SELECT * FROM patrons WHERE id = ?", (patron_id,))
        row = CURSOR.fetchone()
        if row:
            return cls(row[1], row[2], row[3], row[0])
        return None

    @classmethod
    def get_by_id(cls, patron_id):
        return cls.find_by_id(patron_id)

    def _str_(self):
        return f"{self.name} (Email: {self.email}, Phone: {self.phone})"