import sqlite3

class Contact:
    def __init__(self, nom="", prenom="", email="", numero=0, id=0, is_favorite=False):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.numero = numero
        self.id = id
        self.is_favorite = is_favorite

    def create_table_contact(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='Contacts' ''')
            if cursor.fetchone() is None:
                
                cursor.execute('''
                CREATE TABLE Contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    numero INTEGER,
                    is_favorite BOOLEAN DEFAULT 0
                )
                ''')
            else:
                
                cursor.execute('''PRAGMA table_info(Contacts)''')
                columns = [column[1] for column in cursor.fetchall()]
                if 'is_favorite' not in columns:
                   
                    cursor.execute('''ALTER TABLE Contacts ADD COLUMN is_favorite BOOLEAN DEFAULT 0''')
            conn.commit()

    def create_contact(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO Contacts (nom, prenom, email, numero, is_favorite)
                VALUES (?, ?, ?, ?, ?)
                ''', (self.nom, self.prenom, self.email, self.numero, self.is_favorite))
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError("A contact with this email already exists.")

    def read_contacts():
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Contacts")
            return cursor.fetchall()

    def read_favorites():
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Contacts WHERE is_favorite = 1")
            return cursor.fetchall()

 
    def toggle_favorite(self, contact_id):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE Contacts 
            SET is_favorite = CASE WHEN is_favorite = 1 THEN 0 ELSE 1 END 
            WHERE id = ?
            ''', (contact_id,))
            conn.commit()

class Group:
    def __init__(self, nom="", description="", id=0):
        self.nom = nom
        self.description = description
        self.id = id


    def create_table_group():
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                description TEXT
            )
            ''')
            conn.commit()

    def create_group(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO Groups (nom, description)
                VALUES (?, ?)
                ''', (self.nom, self.description))
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"A group with name '{self.nom}' already exists.")


    def read_groups():
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Groups")
            return cursor.fetchall()


    def get_group_members(self, group_id):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT c.* FROM Contacts c
            JOIN ContactGroups cg ON c.id = cg.contact_id
            WHERE cg.group_id = ?
            ''', (group_id,))
            return cursor.fetchall()

class ContactGroup:
    def __init__(self, contact_id=0, group_id=0):
        self.contact_id = contact_id
        self.group_id = group_id

  
    def create_table():
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ContactGroups (
                contact_id INTEGER,
                group_id INTEGER,
                PRIMARY KEY (contact_id, group_id),
                FOREIGN KEY (contact_id) REFERENCES Contacts(id),
                FOREIGN KEY (group_id) REFERENCES Groups(id)
            )
            ''')
            conn.commit()

    def add_contact_to_group(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO ContactGroups (contact_id, group_id)
                VALUES (?, ?)
                ''', (self.contact_id, self.group_id))
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError("This contact is already in the group or invalid IDs.")

    def remove_from_group(self, contact_id, group_id):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM ContactGroups 
            WHERE contact_id = ? AND group_id = ?
            ''', (contact_id, group_id))
            conn.commit()


    def read_contact_groups(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT cg.contact_id, c.nom, c.prenom, cg.group_id, g.nom
            FROM ContactGroups cg
            JOIN Contacts c ON cg.contact_id = c.id
            JOIN Groups g ON cg.group_id = g.id
            ''')
            return cursor.fetchall()