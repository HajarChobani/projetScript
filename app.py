from flask import Flask, redirect, render_template, request, url_for
from models import Contact, Group, ContactGroup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        data = request.form
        try:
            contact = Contact(
                nom=data.get('nom'),
                prenom=data.get('prenom'),
                email=data.get('email'),
                numero=data.get('numero'),
                is_favorite=bool(data.get('is_favorite'))
            )
            contact.create_contact()
        except ValueError as e:
            return str(e), 400
        return redirect('/contacts')

    contacts = Contact.read_contacts()
    return render_template('contacts.html', contacts=contacts)

@app.route('/favorites')
def favorites():
    favorites = Contact.read_favorites()
    return render_template('favorites.html', favorites=favorites)

@app.route('/toggle-favorite/<int:contact_id>')
def toggle_favorite(contact_id):
    Contact.toggle_favorite(contact_id)
    return redirect(request.referrer or url_for('contacts'))

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if request.method == 'POST':
        data = request.form
        try:
            group = Group(
                nom=data.get('nom'),
                description=data.get('description')
            )
            group.create_group()
        except ValueError as e:
            return str(e), 400
        return redirect('/groups')

    groups = Group.read_groups()
    return render_template('groups.html', groups=groups)

@app.route('/group/<int:group_id>')
def group_details(group_id):
    group = Group.read_groups()[group_id - 1]
    members = Group.get_group_members(group_id)
    all_contacts = Contact.read_contacts()
    return render_template('group_details.html', group=group, members=members, contacts=all_contacts)

@app.route('/add-to-group/<int:group_id>', methods=['POST'])
def add_to_group(group_id):
    contact_id = request.form.get('contact_id')
    try:
        contact_group = ContactGroup(contact_id=contact_id, group_id=group_id)
        contact_group.add_contact_to_group()
    except ValueError as e:
        return str(e), 400
    return redirect(url_for('group_details', group_id=group_id))

@app.route('/remove-from-group/<int:group_id>/<int:contact_id>')
def remove_from_group(group_id, contact_id):
    ContactGroup.remove_from_group(contact_id, group_id)
    return redirect(url_for('group_details', group_id=group_id))

if __name__ == '__main__':

    app.run(debug=True)