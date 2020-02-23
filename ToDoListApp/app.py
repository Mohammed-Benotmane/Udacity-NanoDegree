from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres@localhost:5432/udacity'
app.cofig['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class ToDoList(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(), nullable= False)
    def __repr__(self):
        return f'< ToDo ID: {self.id} , description : {self.description} >'

db.create_all()

@app.route('/')
def index():
    return render_template('index.html',data=ToDoList.query.all())
    