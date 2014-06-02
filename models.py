from google.appengine.ext import db

class Teacher(db.Model):
	picture = db.StringProperty()
	rating = db.IntegerProperty(default=1400)
	name = db.StringProperty()
	number = db.IntegerProperty()