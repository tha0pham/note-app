from database import db
import datetime as datetime

class Note(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	title = db.Column("title", db.String(200))
	text = db.Column("text", db.String(100))
	date = db.Column("date", db.String(50))
	last_modified = db.Column("last_modified", db.String(50))
	is_favorite = db.Column("is_favorite", db.Boolean())
	# can create a foreign key; referencing the id variable in the User class, so that is why it is lowercase u
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)
	
	def __init__(self, title, text, date, user_id):
		self.title = title
		self.text = text
		self.date = date
		self.last_modified = date
		self.user_id = user_id
		self.is_favorite = False

class User(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	firstname = db.Column("firstname", db.String(100))
	lastname = db.Column("lastname", db.String(100))
	email = db.Column("email", db.String(100))
	password = db.Column(db.String(255), nullable=False)
	registered_on = db.Column(db.DateTime, nullable=False)
	notes = db.relationship("Note", backref="user", lazy=True)
	comments=db.relationship("Comment", backref="user", lazy=True)

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = password
		self.registered_on = datetime.date.today()
		
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.VARCHAR, nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, text, note_id, user_id):
        self.created_date = datetime.date.today()
        self.text = text
        self.note_id = note_id
        self.user_id = user_id
