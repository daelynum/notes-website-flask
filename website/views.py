from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)


# route for homepage
@views.route('/', methods=['GET', 'POST'])
# until the user logs in, he will not see the home page
@login_required
def home():
    # get the POST method from the home page and add the text with the id 'note' to the note variable
    if request.method == 'POST':
        note = request.form.get('note')
        # flash the errors
        if len(note) < 1:
            flash('note is too short', category='error')
        else:
            # add new note to DB
            new_note = Note(data=note, user_id=current_user.id)
            flash('Note added', category='success')
            db.session.add(new_note)
            db.session.commit()
    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # get data from the POST request (JS passed it as a string) and translate it into json
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    # check if the record exists with the transferred IT specialist
    if note:
        # if it exists and belongs to the current user, delete it from the database
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            # serializing data to JavaScript Object Notation (JSON) format
            return jsonify({})
