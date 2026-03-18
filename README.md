# Gestionnaire de Contacts et de Groupes – Flask & SQLite

Ce projet est une application web permettant de gérer des contacts, des groupes et les relations entre eux.  
Elle a été développée avec **Flask** pour le backend et **SQLite** comme base de données relationnelle.

---

## Fonctionnalités principales

### Gestion des contacts
- Ajouter un contact  
- Modifier un contact  
- Supprimer un contact  
- Consulter les informations (nom, prénom, email, téléphone)

### Favoris
- Marquer un contact comme favori  
- Afficher uniquement les contacts favoris

### Gestion des groupes
- Créer un groupe  
- Modifier un groupe  
- Supprimer un groupe  
- Consulter la liste des groupes

### Relations Contact–Groupe
- Ajouter un contact dans un groupe  
- Retirer un contact d’un groupe  
- Voir les membres d’un groupe

### Interface web conviviale
- Templates HTML avec **Jinja2**  
- Navigation simple et intuitive

### Base de données relationnelle
Trois tables principales :
- **Contacts**
- **Groupes**
- **ContactGroup** (table de relation)

---

## Technologies utilisées

- **Python**
- **Flask**
- **SQLite**
- **HTML / CSS**
- **Jinja2**
- **Tables relationnelles & clés étrangères**



