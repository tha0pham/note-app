# imports
import os

from flask import Flask, render_template

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
