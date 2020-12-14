import os
import traceback

import bcrypt as bcrypt
from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import session

from database import db
from forms import RegisterForm, LoginForm, CommentForm
from models import Comment as Comment
from models import Note as Note
from models import User as User

app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()  # run under the app context


@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return redirect(url_for('get_notes'))
    else:
        return render_template('index.html')


@app.route('/notes')
def get_notes():
    # retrieve user from the database
    # check if a user is saved in session
    if session.get('user'):
        # retrieve notes from the database

        my_notes = db.session.query(Note).filter_by(
            user_id=session['user_id']).all()

        return render_template('notes.html', notes=my_notes,
                               user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/public')
def get_public_notes():
    # retrieve user from the database
    # check if a user is saved in session
    if session.get('user'):
        # retrieve notes from the database
        my_notes = db.session.query(Note.id, Note.title, Note.date,
                                    User.firstname, User.lastname).join(
            Note).filter(
            Note.user_id == User.id).filter_by(is_published=True).all()
        return render_template('public_notes.html', notes=my_notes,
                               user=session[
                                   'user'])
    else:
        return redirect(url_for('login'))


@app.route('/notes/favorite')
def get_favorite_notes():
    # retrieve user from the database
    # check if a user is saved in session
    if session.get('user'):
        # retrieve notes from the database
        my_notes = db.session.query(Note).filter_by(
            user_id=session['user_id'], is_favorite=True).all()
        return render_template('favorites.html', notes=my_notes,
                               user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['noteText']

            from datetime import date
            today = date.today()
            today = today.strftime('%Y-%m-%d')

            newEntry = Note(title, text, today, user_id=session['user_id'])
            db.session.add(newEntry)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            # get request - show new note form
            return render_template('new.html', user=session['user'])
    else:
        # user is not in session; redirect to login
        return redirect(url_for('login'))


@app.route('/notes/<note_id>')
def get_note(note_id):
    # retrieve note from DB
    note = db.session.query(Note).filter_by(id=note_id).one()
    comments = db.session.query(Comment.id, Comment.created_date, Comment.text,
                                Comment.user_id, User.firstname,
                                User.lastname).join(
        Comment).filter(
        Comment.user_id == User.id).filter_by(note_id=note_id).all()
    if session.get('user') and (session['user_id'] == note.user_id or
                                note.is_published):
        # create a comment form object
        form = CommentForm()
        return render_template('note.html', note=note, comments=comments,
                               form=form, user=session['user'])
    elif session.get('user'):
        return redirect(url_for('get_public_notes'))
    else:
        return redirect(url_for('login'))


@app.route('/notes/favorite/<note_id>', methods=['POST'])
def bookmark_note(note_id):
    if session.get('user'):
        note = db.session.query(Note).filter_by(id=note_id).one()

        # allow editing only if user is author
        if session.get('user_id') == note.user_id:
            note.is_favorite = not note.is_favorite
            db.session.commit()
            return {'success': True}, 200
        else:
            return {'error': 'Not authorized'}, 400
    else:
        return redirect(url_for('login'))


@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    # check if a user is saved in session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get note data
            text = request.form['noteText']
            note = db.session.query(Note).filter_by(id=note_id).filter_by(
                user_id=session['user_id']
            ).one()
            # update note data
            note.title = title
            note.text = text
            from datetime import date
            today = date.today()
            today = today.strftime("%Y-%m-%d")
            note.last_modified = today
            # update note in DB
            db.session.add(note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            # GET request - show new note form to edit note
            # retrieve note from database
            my_note = db.session.query(Note).filter_by(id=note_id).filter_by(
                user_id=session['user_id']
            ).one()

            return render_template('new.html', note=my_note,
                                   user=session['user'])
    else:
        # user is not in session; redirect to login
        return redirect(url_for('login'))


@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    # check if user is saved in session
    if session.get('user'):
        # retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).filter_by(
            user_id=session['user_id']
        ).one()
        db.session.delete(my_note)
        db.session.commit()
        return redirect(url_for('get_notes'))
    else:
        return redirect(url_for('login'))


@app.route('/comments/delete/<comment_id>', methods=['POST'])
def delete_comment(comment_id):
    # check if user is saved in session
    if session.get('user'):
        # retrieve note from database
        comment = db.session.query(Comment).filter_by(id=comment_id).one()
        note = db.session.query(Note).filter_by(id=comment.note_id).one()
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('get_note', note_id=note.id))
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # validate_on_submit only validates using POST
    if form.validate_on_submit():
        # form validation included a criteria to check the username does not
        # exist we can know we are safe to add a user to the database
        password_hash = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_record = User(first_name, last_name, request.form['email'],
                          password_hash)
        db.session.add(new_record)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        # get the id of the newly created database record
        the_user = db.session.query(User).filter_by(
            email=request.form['email']).one()
        # save the user's id to the session
        session['user_id'] = the_user.id

        return redirect(url_for('get_notes'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(
            email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'),
                          the_user.password):
            # password match add user info to session
            session['user'] = the_user.firstname
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


@app.route('/notes/<note_id>/comment', methods=['POST'])
def new_comment(note_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(note_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_note', note_id=note_id))

    else:
        return redirect(url_for('login'))


@app.route('/notes/publish/<note_id>', methods=['POST'])
def publish_note(note_id):
    # check if user is saved in session
    if session.get('user'):
        # retrieve note from database
        my_note = db.session.query(Note).filter_by(id=note_id).one()

        # allow editing only if user is author
        if session.get('user_id') == my_note.user_id:
            my_note.is_published = not my_note.is_published
            db.session.commit()
            return {'success': True}, 200
        else:
            return {'error': 'Not authorized'}, 400
    else:
        return redirect(url_for('login'))


@app.errorhandler(Exception)
def get_error_page(e):
    traceback.print_exc()
    return render_template('error.html', e=e)


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(
    os.getenv('PORT', 5000)), debug=True)
