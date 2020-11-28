# imports
import os
from os import name                 # os is used to get environment variables IP & PORT
from flask import Flask, render_template

app = Flask(__name__)     # create an app

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

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(
    os.getenv('PORT', 5000)), debug=True)
