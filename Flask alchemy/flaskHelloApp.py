from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/udacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)
class Person(db.Model):
    __tablename__ = "personnes"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(), nullable=False)
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name} >'


db.create_all()

@app.route('/')
def index():
    person = Person.query.first()
    return 'Hello! '+ person.name
