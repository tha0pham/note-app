# Note App

Note App is a tool that allows users to create and manage their own notes. 
The application includes the following features:
* User account registration / sign-in
* Displays a list of user's notes
* View/edit a note
* Delete note(s)
* Add/delete comments on a note
* Create new notes
* Favoriting notes
* Sorting list of notes
* Make notes public (publish)

## Prerequisites

Before you begin ensure you have met the following requirements:
* You have installed git version 2.22 or higher (https://git-scm.com/downloads)
* You have installed python version 3.6 or higher (https://www.python.org/downloads/)
* You have installed SQLite (version 3 / SQLite3) (https://www.sqlite.org/download.html)
* You have installed Flask web framework
* You have installed wtforms, Flask-WTF, email_validator, and bcrypt

## Installing Note App

To run Note App locally, follow these steps:

In terminal type the following commands:

Create a directory for the note app
```
mkdir note_app
```
Change into the newly created directory
```
cd note_app
```
Clone the project from Github
```
git clone https://github.com/thaopham1816/note-app.git
```
Create a Python virtual environment

```
python3 -m venv venv
```
- MacOS:
```
source venv/bin/activate
```
- Windows:
```
mypthon Scripts activate
```
Install Flask framework
```
pip3 install flask
```
Install SQLAlchemy
```
pip3 install flask-sqlalchemy
```
Install modules and bcrypt
```
pip3 install wtforms
pip3 install Flask-WTF
pip3 install email_validator
pip3 install bcrypt
```
Set flask environment variable 

- MacOS:
```
export FLASK_APP=routes.py
```
- Windows:
```
set FLASK_APP=routes.py
```
Start the Flask server
```
flask run
```
Open web browser and go to
```
http://localhost:5000/
```

## Contributors
* @Thao Pham
* @Wallidortiz
* @Tia-Vang
* @aquinn16
* @egarci26
