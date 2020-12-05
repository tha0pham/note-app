# imports
import os

from flask import Flask, render_template, request

app = Flask(__name__)  # create an app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/notes')
def get_notes():
    return render_template('notes.html')


@app.route('/notes/new')
def new_note():
    return render_template('new.html')


@app.route('/notes/<note_id>')
def get_note(note_id):
    from datetime import date
    today = date.today().strftime('%m-%d-%Y')
    note = {
        'id': '1',
        'title': 'Mock note',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. '
                'Amet in perspiciatis quo reiciendis? Aliquam excepturi explicabo fuga maiores molestias, soluta tempora unde velit? Cupiditate doloremque harum incidunt pariatur porro, tempora?',
        'created_date': today,
        'last_modified': today,
        'is_favorite': True
    }
    comment = {
        'id': 1,
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.',
        'note_id': 1,
        'user_id': 1,
        'created_date': today
    }
    note['comments'] = [comment for c in range(3)]
    return render_template('note.html', note = note)


@app.route('/notes/favorite/<note_id>', methods=['POST'])
def bookmark_note(note_id):
    # request.form['is_bookmarked'] == 'true'
    return "not implemented yet"


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    return "not implemented yet"


@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    return "not implemented yet"


@app.route('/register', methods=['GET', 'POST'])
def register():
    return "not implemented yet"


@app.route('/login', methods=['POST', 'GET'])
def login():
    return "not implemented yet"


@app.route('/logout')
def logout():
    return "not implemented yet"


@app.route('/notes/<note_id>/comment', methods=['POST'])
def new_comment(note_id):
    return "not implemented yet"


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(
    os.getenv('PORT', 5000)), debug=True)
