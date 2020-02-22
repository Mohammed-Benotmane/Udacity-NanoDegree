from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://posgtres:1475963mimo@localhost:5432/udacity'

db = SQLAlchemy(app)
class Person(db.Model):
    __tablename__ = "personnes"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(), nullable= False)

@app.route('/')
def index():
    return 'Hello World!'
