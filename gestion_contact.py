import sqlite3

class Contact:
    def __init__(self, nom="", prenom="", email="", numero=0, id=0):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.numero = numero
        self.id = id

    def create_table_contact(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                numero INTEGER
            )
            ''')
            conn.commit()
        print("Table 'Contacts' créée avec succès.")


    def create_contact(self):  
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO Contacts (nom, prenom, email, numero)
                VALUES (?, ?, ?, ?)
                ''', (self.nom, self.prenom, self.email, self.numero))
                conn.commit()
                print(f"Contact '{self.nom} {self.prenom}' ajouté avec succès.")
            except sqlite3.IntegrityError:
                print("Erreur : Un contact avec cet email existe déjà.")


    def read_contacts(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Contacts")
            contacts = cursor.fetchall()
            if contacts:
                print("Liste des contacts :")
                for contact in contacts:
                    print(contact)
            else:
                print("Aucun contact trouvé.")
            return contacts

    def update_contact(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE Contacts
            SET nom = ?, prenom = ?, email = ?, numero = ?
            WHERE id = ?
            ''', (self.nom, self.prenom, self.email, self.numero, self.id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Contact ID {self.id} mis à jour avec succès.")
            else:
                print(f"Aucun contact trouvé avec l'ID {self.id}.")


    def delete_contact(self,contact_id):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Contacts WHERE id = ?", (contact_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Contact ID {contact_id} supprimé avec succès.")
            else:
                print(f"Aucun contact trouvé avec l'ID {contact_id}.")

contact = Contact()
contact.create_table_contact()


class Groupe:
    def __init__(self, nom="", description="", id=0):
        self.nom = nom
        self.description = description
        self.id = id

    def create_table_group(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Groupes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                description TEXT
            )
            ''')
            conn.commit()
        print("Table 'Groupes' créée avec succès.")

    def create_group(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO Groupes (nom, description)
                VALUES (?, ?)
                ''', (self.nom, self.description))
                conn.commit()
                print(f"Groupe '{self.nom}' ajouté avec succès.")
            except sqlite3.IntegrityError:
                print(f"Erreur : Un groupe avec le nom '{self.nom}' existe déjà.")

    def read_groups(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Groupes")
            groupes = cursor.fetchall()
            if groupes:
                print("Liste des groupes :")
                for groupe in groupes:
                    print(groupe)
            else:
                print("Aucun groupe trouvé.")
            return groupes

    def update_group(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE Groupes
            SET nom = ?, description = ?
            WHERE id = ?
            ''', (self.nom, self.description, self.id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Groupe ID {self.id} mis à jour avec succès.")
            else:
                print(f"Aucun groupe trouvé avec l'ID {self.id}.")

    def delete_group(self,group_id):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Groupes WHERE id = ?", (group_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Groupe ID {group_id} supprimé avec succès.")
            else:
                print(f"Aucun groupe trouvé avec l'ID {group_id}.")

groupe = Groupe()
groupe.create_table_group()

class ContactGroup:
    def __init__(self, contact_id=0, group_id=0, id=0):
        self.contact_id = contact_id
        self.group_id = group_id
        self.id = id

    def create_group_contact(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ContactGroup (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                FOREIGN KEY (contact_id) REFERENCES Contacts(id),
                FOREIGN KEY (group_id) REFERENCES Groupes(id)
            )
            ''')
            conn.commit()
        print("Table 'ContactGroup' créée avec succès.")

    def add_contact_to_group(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO ContactGroup (contact_id, group_id)
                VALUES (?, ?)
                ''', (self.contact_id, self.group_id))
                conn.commit()
                print(f"Contact ID {self.contact_id} ajouté au Groupe ID {self.group_id}.")
            except sqlite3.IntegrityError:
                print("Erreur : Ce contact est déjà dans ce groupe ou les IDs sont invalides.")

    def read_contact_groups(self):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT cg.id, c.nom, c.prenom, g.nom 
            FROM ContactGroup cg
            JOIN Contacts c ON cg.contact_id = c.id
            JOIN Groupes g ON cg.group_id = g.id
            ''')
            relations = cursor.fetchall()
            if relations:
                print("Relations Contact-Groupe :")
                for relation in relations:
                    print(relation)
            else:
                print("Aucune relation trouvée.")
            return relations

    def update_contact_group(self, new_contact_id, new_group_id):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE ContactGroup
            SET contact_id = ?, group_id = ?
            WHERE id = ?
            ''', (new_contact_id, new_group_id, self.id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Relation ID {self.id} mise à jour avec succès.")
            else:
                print(f"Aucune relation trouvée avec l'ID {self.id}.")

    def delete_contact_group(self, relation_id):
        with sqlite3.connect("app_contact.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ContactGroup WHERE id = ?", (relation_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Relation ID {relation_id} supprimée avec succès.")
            else:
                print(f"Aucune relation trouvée avec l'ID {relation_id}.")

group_contact = ContactGroup()
group_contact.create_group_contact()
    
