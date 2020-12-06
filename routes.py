# imports
import os
import bcrypt
from flask import Flask, render_template, redirect, url_for, request, session
from forms import RegisterForm, LoginForm
from models import User as User

app = Flask(__name__)  # create an app
app.config['SECRET_KEY'] = 'SE3155'

@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return redirect(url_for('get_notes'))
    else:
        return render_template('index.html')


@app.route('/notes')
def get_notes():
    if session.get('user'):
        return render_template('notes.html', user=session['user'])
    else:
        return redirect(url_for('index'))


@app.route('/notes/new')
def new_note():
    if session.get('user'):
        return render_template('new.html', user=session['user'])
    else:
        return redirect(url_for('index'))


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
    if session.get('user'):
        return redirect(url_for('get_notes'))
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            password_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
            first_name = request.form['firstname']
            session['user'] = first_name
            last_name = request.form['lastname']
            email = request.form['email']
            newUser = User(first_name, last_name, email, password_hash)
            return redirect(url_for('get_notes'))
        return render_template('register.html', form=form)



@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('user'):
        return redirect(url_for('get_notes'))
    else:
        login_form = LoginForm()
        # validate_on_submit only validates using POST
        if login_form.validate_on_submit():
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            user = User('', '', email, password)
            session['user'] = request.form['email']
            if login_form.password.errors:
                login_form.password.errors = ["Incorrect username or password."]
                return render_template("login.html", form=login_form)
            else:
                return redirect(url_for('get_notes'))
        else:
             # form did not validate or GET request
            return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    session['user'] = ''
    return redirect(url_for('index'))


@app.route('/notes/<note_id>/comment', methods=['POST'])
def new_comment(note_id):
    return "not implemented yet"


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(
    os.getenv('PORT', 5000)), debug=True)
