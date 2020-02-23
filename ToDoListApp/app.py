from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(), nullable= False)
    def __repr__(self):
        return f'< ToDo ID: {self.id} , description : {self.description} >'

@app.route('/')
def index():
    return render_template('index.html',data=[{
        'description': 'todo1'
    },
    {
        'description': 'todo2'
    },
    {
        'description': 'todo3'
    },
    ])
    